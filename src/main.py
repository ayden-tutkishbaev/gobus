from fastapi import FastAPI
from database.core import create_tables
from contextlib import asynccontextmanager

from auth.api import user

import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await drop_tables()
    await create_tables()
    print("Base is functioning!")
    yield
    print("OFF")
    

app = FastAPI(lifespan=lifespan)

app.include_router(user, prefix="/api/users", tags=['users'])


if __name__ == '__main__':
    uvicorn.run("main:app")



# @app.post('/schools/add', response_model=SchoolCreate, status_code=status.HTTP_201_CREATED)
# async def add_school(school: SchoolCreate, db: db_connection):
#     new_school = School(name=school.name)
#     db.add(new_school)
#     await db.commit()
#     await db.refresh(new_school)
#     return new_school
    
    
# @app.get('/schools/get_all')
# async def get_all_schools(db: db_connection):
#     schools = await db.scalars(select(School))
#     return schools.all()



