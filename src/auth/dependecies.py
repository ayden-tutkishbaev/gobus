from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from database.core import get_db


db_connection = Annotated[AsyncSession, Depends(get_db)]