import uuid

from fastapi import HTTPException, status

from src.database.core import session
from src.auth.models import User
from src.auth.security import hash_password
from src.auth.enum import Role
from src.config import config

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def add_superadmin():
    async with session() as conn:
        username = await conn.execute(
            select(User.username).where(User.username == config.SUPERADMIN_USERNAME)
        )
        
        if username.scalar_one_or_none() == config.SUPERADMIN_USERNAME:
            print("Superuser is on its place! :)")
        
        else:
            conn.add(User(
                username=config.SUPERADMIN_USERNAME,
                phone_number=config.SUPERADMIN_PHONE_NUMBER,
                role=Role.SUPERADMIN,
                password_hashed=hash_password(config.SUPERADMIN_PASSWORD),
            ))
            await conn.commit()
            print("Superuser has been created succesfully!")
            

# async def get_or_404(db: AsyncSession, model, obj_id: uuid.UUID):
#     result = await db.execute(select(model).where(model.id == obj_id))
#     obj = result.scalar_one_or_none()
#     if not obj:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, f"{model.__tablename__} not found")
#     return obj


# async def apply_updates(db: AsyncSession, obj, data):
#     update_data = data.model_dump(exclude_unset=True)
#     if not update_data:
#         raise HTTPException(status.HTTP_400_BAD_REQUEST, "No fields to update")
#     for field, value in update_data.items():
#         setattr(obj, field, value)
#     await db.commit()
#     await db.refresh(obj)
#     return obj