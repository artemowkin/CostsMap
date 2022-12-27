import redis.asyncio as redis

from .settings import settings


redis_db = redis.Redis.from_url(settings.redis_url)
