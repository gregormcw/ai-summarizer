import hashlib
import json
from typing import Optional

import redis

from app.core.config import get_settings
from app.core.logging import logger


class CacheService:
    """Redis cache for storing summaries."""

    def __init__(self):
        settings = get_settings()
        self.redis_client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            decode_responses=True,
        )

    def _generate_cache_key(self, text: str, style: str, max_length: int) -> str:
        """Generate a unique cache key by hashing inputs."""
        combined = f"{text}:{style}:{max_length}"
        hash_object = hashlib.sha256(combined.encode())
        cache_key = hash_object.hexdigest()
        return cache_key

    def get(self, text: str, style: str, max_length: int) -> Optional[dict]:
        """Get cached summary if it exists."""
        try:
            cache_key = self._generate_cache_key(
                text=text, style=style, max_length=max_length
            )
            summary_text = self.redis_client.get(cache_key)
            if summary_text:
                return json.loads(summary_text)
            return None
        except redis.RedisError as e:
            logger.error(f"Redis error: {e}")
            return None

    def set(self, text: str, style: str, max_length: int, summary_data: dict) -> None:
        """Store summary in cache with TTL."""
        try:
            cache_key = self._generate_cache_key(
                text=text, style=style, max_length=max_length
            )
            summary_text = json.dumps(summary_data)
            settings = get_settings()
            self.redis_client.set(
                name=cache_key, value=summary_text, ex=settings.cache_ttl
            )
        except redis.RedisError as e:
            logger.error(f"Redis error: {e}")
