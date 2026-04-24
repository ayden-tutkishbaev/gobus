from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config_manager import config


url = URL.create(
    "postgresql+asyncpg",
    host=config.DB_HOST,
    username=config.DB_USER,
    password=config.DB_PASSWORD,
    port=config.DB_PORT,
    database=config.DB_NAME
)


engine = create_async_engine(
    url=url, echo=True
)

session = async_sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with session() as db:
        yield db