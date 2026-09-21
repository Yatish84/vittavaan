"""Safe structured logging foundation."""

import logging
import sys
from collections.abc import MutableMapping
from typing import Any

import structlog

SENSITIVE_KEY_PARTS = (
    "authorization",
    "cookie",
    "credential",
    "database_url",
    "password",
    "redis_url",
    "secret",
    "token",
)


def redact_sensitive_fields(
    _logger: object, _method_name: str, event_dict: MutableMapping[str, Any]
) -> MutableMapping[str, Any]:
    """Redact sensitive values by key before any renderer receives them."""

    def redact(value: Any) -> Any:
        if isinstance(value, dict):
            return {
                key: "[REDACTED]"
                if any(part in key.lower() for part in SENSITIVE_KEY_PARTS)
                else redact(nested)
                for key, nested in value.items()
            }
        if isinstance(value, (list, tuple)):
            return [redact(item) for item in value]
        return value

    return {
        key: "[REDACTED]"
        if any(part in key.lower() for part in SENSITIVE_KEY_PARTS)
        else redact(value)
        for key, value in event_dict.items()
    }


def configure_logging() -> None:
    """Configure JSON logs without rendering application secret values."""

    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.INFO)
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            redact_sensitive_fields,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    )
