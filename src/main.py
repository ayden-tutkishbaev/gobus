from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.database.tools import create_tables, drop_tables, drop_pk
from src.admin.services import add_superadmin

from src.auth.router import user  
from src.admin.routers.kids import admin_kid
from src.admin.routers.contracts import admin_contract
from src.admin.routers.parents import admin_parent
from src.admin.routers.routes import admin_route
from src.admin.routers.schools import admin_school
from src.admin.routers.staff import admin_staff
from src.admin.routers.teachers import admin_teacher
from src.admin.routers.transport import admin_transport
from src.admin.routers.schedules import admin_schedule

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

app.include_router(user, prefix="/api/v1/users", tags=['Users'])
app.include_router(superadmin, prefix="/api/v1/superadmin", tags=['Superadmin'])
app.include_router(admin_kid, prefix="/api/v1/admins", tags=['Admins'])
app.include_router(admin_contract, prefix="/api/v1/admins", tags=['Admins'])
app.include_router(admin_parent, prefix="/api/v1/admins", tags=['Admins'])
app.include_router(admin_route, prefix="/api/v1/admins", tags=['Admins'])
app.include_router(admin_school, prefix="/api/v1/admins", tags=['Admins'])
app.include_router(admin_staff, prefix="/api/v1/admins", tags=['Admins'])
app.include_router(admin_teacher, prefix="/api/v1/admins", tags=['Admins'])
app.include_router(admin_transport, prefix="/api/v1/admins", tags=['Admins'])
app.include_router(admin_schedule, prefix="/api/v1/admins", tags=['Admins'])


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
    