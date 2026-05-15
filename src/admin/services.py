from src.database.core import session
from src.auth.models import User
from src.auth.enum import Role
from src.config import config
from src.core.security import hash_password

from sqlalchemy import select


async def add_superadmin():
    async with session() as conn:
        username = await conn.execute(
            select(User.username).where(User.username == config.SUPER_ADMIN_USERNAME)
        )
        
        if username.scalar_one_or_none() == config.SUPER_ADMIN_USERNAME:
            print("Superuser is on its place! :)")
        
        else:
            conn.add(User(
                username=config.SUPER_ADMIN_USERNAME,
                phone_number=config.SUPER_ADMIN_PHONE_NUMBER,
                role=Role.SUPERADMIN,
                password_hashed=hash_password(config.SUPER_ADMIN_PASSWORD),
            ))
            await conn.commit()
            print("Superuser has been created succesfully!")
            