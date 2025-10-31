import hashlib
import json
from typing import Any, Optional

from redis import Redis

from .config import settings


_redis_client: Optional[Redis] = None


def get_redis() -> Optional[Redis]:
    global _redis_client
    if _redis_client is not None:
        return _redis_client
    if not settings.redis_url:
        return None
    _redis_client = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis_client


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def cache_get(key: str) -> Optional[dict[str, Any]]:
    client = get_redis()
    if not client:
        return None
    raw = client.get(key)
    return json.loads(raw) if raw else None


def cache_set(key: str, value: dict[str, Any]) -> None:
    client = get_redis()
    if not client:
        return
    ttl_seconds = settings.cache_ttl_days * 24 * 60 * 60
    client.setex(key, ttl_seconds, json.dumps(value))


def rate_limit_allow(device_id: str) -> bool:
    """Allow request if under RATE_LIMIT_RPM for this device. Uses Redis if available.
    Fallback: always allow when Redis is not configured.
    """
    client = get_redis()
    if not client:
        return True
    key = f"ratelimit:{device_id}:{int(__import__('time').time() // 60)}"
    count = client.incr(key)
    if count == 1:
        client.expire(key, 60)
    return count <= settings.rate_limit_rpm


