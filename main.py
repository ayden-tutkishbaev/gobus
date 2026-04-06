from fastapi import FastAPI, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.core import engine, Base, create_tables, drop_tables, get_db
from database.schemas import SchoolCreate
from database.models import *

from typing import Annotated

from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("Base is functioning!")
    yield
    print("OFF")
    

db_connection = Annotated[AsyncSession, Depends(get_db)]

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def main_func():
    return "Hi!"


@app.post('/schools/add', response_model=SchoolCreate, status_code=status.HTTP_201_CREATED)
async def add_school(school: SchoolCreate, db: db_connection):
    new_school = School(name=school.name)
    db.add(new_school)
    await db.commit()
    await db.refresh(new_school)
    return new_school
    
    
@app.get('/schools/get_all')
async def get_all_schools(db: db_connection):
    schools = await db.scalars(select(School))
    return schools.all()