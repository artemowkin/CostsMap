import aioredis

from .settings import settings


redis_db = aioredis.from_url(settings.redis_url)
