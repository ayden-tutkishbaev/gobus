from datetime import datetime, date
from zoneinfo import ZoneInfo
from database.core import Base, engine


def tashkent_now():
    return datetime.now(ZoneInfo("Asia/Tashkent"))


def tashkent_today():
    return tashkent_now().date()   


async def create_tables():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)
        
        
async def drop_tables():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.drop_all)