import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.auth.models import User


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    result = await session.execute(
        select(User).where(User.username == username)
    )
    return result.scalars().first()


async def get_user_by_id(session: AsyncSession, user_id: uuid.UUID) -> User | None:
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalars().first()