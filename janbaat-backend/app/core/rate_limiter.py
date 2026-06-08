from fastapi import Request

from app.config import settings
from app.core.cache import cache_incr
from app.core.exceptions import RateLimitError


async def check_rate_limit(request: Request, user_id: str) -> None:
    """
    Sliding window rate limiter using Redis INCR.
    Keyed per user per minute.
    """
    key = f"rate:{user_id}:{_current_minute()}"
    count = await cache_incr(key, ttl=60)
    if count > settings.rate_limit_per_minute:
        raise RateLimitError()


def _current_minute() -> str:
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)
    return now.strftime("%Y%m%d%H%M")
