"""
CLI entry point for data ingestion.

Usage:
    python -m app.ingestion.cli                    # One-shot ingestion
    python -m app.ingestion.cli --interval 60      # Continuous (every 60s)
    python -m app.ingestion.cli --bridge OBJ-001 --tunnel OBJ-004
"""

import asyncio
import logging

from app.ingestion.pipeline import IngestionPipeline


async def main(args: list[str] = None) -> None:
    import argparse

    parser = argparse.ArgumentParser(description="BridgeWatch AI Data Ingestion")
    parser.add_argument("--interval", type=int, default=0, help="Polling interval in seconds (0 = one-shot)")
    parser.add_argument("--bridge", default="OBJ-20260508-001", help="Bridge object ID")
    parser.add_argument("--large-bridge", default="OBJ-20260508-003", help="Large bridge object ID")
    parser.add_argument("--tunnel", default="OBJ-20260508-004", help="Tunnel object ID")
    parsed = parser.parse_args(args)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    pipeline = IngestionPipeline()
    if parsed.interval > 0:
        logger = logging.getLogger(__name__)
        logger.info("Starting continuous ingestion every %ds...", parsed.interval)
        await pipeline.start(interval=parsed.interval)
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            await pipeline.stop()
    else:
        counts = await pipeline.run_once(
            bridge_id=parsed.bridge,
            large_bridge_id=parsed.large_bridge,
            tunnel_id=parsed.tunnel,
        )
        print(f"Ingestion complete: {counts}")


if __name__ == "__main__":
    asyncio.run(main())
