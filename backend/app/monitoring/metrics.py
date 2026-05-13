"""
Prometheus metrics registry for BridgeWatch AI.

Centralizes all application metrics so they can be updated from
any part of the codebase and exposed at the /metrics endpoint.
"""

from prometheus_client import Counter, Gauge, Histogram, generate_latest

# ── HTTP request metrics ───────────────────────────────────────────

HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests",
    labelnames=["method", "endpoint", "status"],
)

HTTP_REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    labelnames=["method", "endpoint"],
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
)

# ── Business metrics ───────────────────────────────────────────────

EVENTS_TOTAL = Gauge(
    "bridgewatch_events_total",
    "Total events by risk level",
    labelnames=["risk_level"],
)

ALERTS_UNREAD = Gauge(
    "bridgewatch_alerts_unread_total",
    "Number of unread alerts",
)

WORKER_ACTIVE = Gauge(
    "bridgewatch_worker_active",
    "Whether the inference worker is running (1=yes, 0=no)",
)

INFERENCE_TASKS_TOTAL = Counter(
    "bridgewatch_inference_tasks_total",
    "Total inference tasks processed",
    labelnames=["status"],
)

# ── Helper ─────────────────────────────────────────────────────────

def get_metrics() -> bytes:
    """Return the latest Prometheus metrics in text format."""
    return generate_latest()
