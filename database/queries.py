from database.core import session
from api.auth.models import User
from config_manager import config
from api.auth.utils import hash_password

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
                password=hash_password(config.SUPER_ADMIN_PASSWORD),
                is_superadmin=True
            ))
            await conn.commit()
            print("Superuser has been created succesfully!")
            
            