from fastapi import FastAPI
from contextlib import asynccontextmanager

from database.tools import create_tables, drop_tables
from database.queries import add_superadmin

from api.auth.users import user
from api.admin.admins import admin

import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await drop_tables()
    await create_tables()
    await add_superadmin()
    print("Database has begun its operation!")
    yield
    print("OFF")
    

app = FastAPI(lifespan=lifespan)

app.include_router(user, prefix="/api/users", tags=['Users'])
app.include_router(admin, prefix="/api/admins", tags=['Admins'])


if __name__ == '__main__':
    uvicorn.run("main:app")
    