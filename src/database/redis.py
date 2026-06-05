import redis.asyncio as aioredis
from src.config import config

redis_client: aioredis.Redis | None = None


async def init_redis() -> aioredis.Redis:
    return aioredis.from_url(
        url=f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}",
        decode_responses=True
    )

async def get_redis() -> aioredis.Redis:
    return redis_client