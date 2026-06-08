import json
from typing import Any

import redis.asyncio as aioredis

from app.config import settings

_redis: aioredis.Redis | None = None


def get_redis() -> aioredis.Redis:
    global _redis
    if _redis is None:
        _redis = aioredis.from_url(settings.redis_url, decode_responses=True)
    return _redis


async def ping_redis() -> bool:
    return await get_redis().ping()


async def cache_get(key: str) -> Any | None:
    data = await get_redis().get(key)
    if data is None:
        return None
    return json.loads(data)


async def cache_set(key: str, value: Any, ttl: int) -> None:
    await get_redis().setex(key, ttl, json.dumps(value))


async def cache_delete(key: str) -> None:
    await get_redis().delete(key)


async def cache_delete_pattern(pattern: str) -> None:
    keys = await get_redis().keys(pattern)
    if keys:
        await get_redis().delete(*keys)


async def cache_incr(key: str, ttl: int | None = None) -> int:
    r = get_redis()
    count = await r.incr(key)
    if ttl and count == 1:
        await r.expire(key, ttl)
    return count
