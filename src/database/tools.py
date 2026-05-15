from src.database.core import Base, engine
from datetime import datetime
from zoneinfo import ZoneInfo
from sqlalchemy import text


def tashkent_now():
    return datetime.now(ZoneInfo("Asia/Tashkent"))


def tashkent_today():
    return tashkent_now().date()   


async def drop_pk():
    async with engine.begin() as conn:
        await conn.execute(text("DROP SCHEMA public CASCADE"))
        await conn.execute(text("CREATE SCHEMA public"))

async def create_tables():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)
        
        
async def drop_tables():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.drop_all)