"""Centralized rate limiter configuration."""
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.config.settings import settings


def _get_storage_uri() -> str:
    """Choose storage backend for rate limits."""
    if settings.RATE_LIMIT_STORAGE_URI:
        return settings.RATE_LIMIT_STORAGE_URI
    if settings.REDIS_URL:
        return settings.REDIS_URL
    return "memory://"


limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[],
    storage_uri=_get_storage_uri(),
)

