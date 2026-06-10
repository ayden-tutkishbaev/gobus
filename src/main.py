from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.admin.routers.admin import admin_router
from src.staff.routers import staff_router
from src.database.tools import create_tables, drop_tables, drop_pk
from src.admin.services import add_superadmin
from src.config import config

from src.auth.router import user  

from src.admin.routers.superadmin import superadmin  
from src.database.redis import init_redis
import src.database.redis as redis_state

import uvicorn

import src.models


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await drop_pk()
    # await drop_tables()
    await create_tables()
    await add_superadmin()
    
    redis_state.redis_client = await init_redis()
    print("Database has begun its operation!")
    yield
    
    await redis_state.redis_client.aclose()
    print("OFF")
    

app = FastAPI(title="GoBus API", lifespan=lifespan, version="1.0.0")

app.include_router(user, prefix=config.api_v1_prefix)
app.include_router(superadmin, prefix=config.api_v1_prefix)
app.include_router(admin_router, prefix=config.api_v1_prefix)
app.include_router(staff_router, prefix=config.api_v1_prefix)


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
    