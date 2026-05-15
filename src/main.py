from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.database.tools import create_tables, drop_tables, drop_pk
from src.admin.services import add_superadmin

from src.auth.router import user  # EDIT
from src.admin.admin import admin  # EDIT
from src.admin.superadmin import superadmin  # EDIT

import uvicorn

import src.models


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await drop_pk()
    # await drop_tables()
    await create_tables()
    await add_superadmin()
    print("Database has begun its operation!")
    yield
    print("OFF")
    

app = FastAPI(title="GoBus API", lifespan=lifespan, version="1.0.0")

app.include_router(user, prefix="/api/v1/users", tags=['Users'])
app.include_router(superadmin, prefix="/api/v1/superadmin", tags=['Superadmin'])
app.include_router(admin, prefix="/api/v1/admins", tags=['Admins'])


if __name__ == '__main__':
    uvicorn.run("main:app")
    