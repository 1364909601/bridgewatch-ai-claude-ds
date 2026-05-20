import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base
from app.models import *  # noqa: F401 — register all ORM models before create_all
from app.utils.exceptions import register_exception_handlers
from app.middleware.logging_mw import LoggingMiddleware
from app.middleware.prometheus_mw import PrometheusMiddleware
from app.api.router import api_router
from app.engine.worker import InferenceWorker

import logging
logger = logging.getLogger(__name__)


async def _escalation_loop():
    """Background task: periodically check for unacknowledged events and escalate."""
    from app.database import async_session_factory
    from app.services.alert_service import AlertService
    while True:
        try:
            async with async_session_factory() as db:
                await AlertService.check_escalations(db)
                await db.commit()
        except Exception:
            logger.exception("Escalation check failed")
        await asyncio.sleep(60)  # check every 60 seconds


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup: create tables and run dev migrations
    if settings.DEBUG:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        from app.utils.migration import migrate_dev_database
        await migrate_dev_database(engine)

    # Start background inference worker
    worker = InferenceWorker(poll_interval=settings.WORKER_POLL_INTERVAL)
    if settings.WORKER_ENABLED:
        await worker.start()
        app.state._inference_worker = worker
    else:
        app.state._inference_worker = None
        logger.info("Inference worker disabled by config")

    # Start escalation check loop
    escalation_task = asyncio.create_task(_escalation_loop(), name="escalation-loop")
    app.state._escalation_task = escalation_task

    # Seed default users in dev mode
    if settings.DEBUG:
        try:
            from app.database import async_session_factory
            from app.services.auth_service import AuthService
            async with async_session_factory() as db:
                await AuthService.seed_users(db)
                await db.commit()
        except Exception:
            logger.exception("Failed to seed users")

    yield

    # Shutdown: stop workers first, then dispose engine
    escalation_task.cancel()
    try:
        await escalation_task
    except asyncio.CancelledError:
        pass
    if settings.WORKER_ENABLED:
        await worker.stop()
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
app.add_middleware(PrometheusMiddleware)
app.add_middleware(LoggingMiddleware)

# Exception handlers
register_exception_handlers(app)

# API routes
app.include_router(api_router, prefix="/api")
