from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.core import get_db

from src.database.redis import get_redis
from redis.asyncio import Redis

db_connection = Annotated[AsyncSession, Depends(get_db)]
redis_connection = Annotated[Redis, Depends(get_redis)]