from typing import Annotated
import uuid 
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.enum import Role
from src.auth.schemas import UserSchema
from src.auth.services import ACCESS_TOKEN_TYPE, get_auth_user_from_token_of_type
from src.database.core import get_db
from src.auth.models import User

from fastapi import Depends, HTTPException, status


# async def get_current_user(
#     # token: Annotated[str, Depends(oauth2_scheme)],
#     db: Annotated[AsyncSession, Depends(get_db)],
# ) -> User:
#     # user_id = verify_access_token(token)
#     # if user_id is None:
#     #     raise HTTPException(
#     #         status_code=status.HTTP_401_UNAUTHORIZED,
#     #         detail='Invalid or expired token',
#     #         headers={'WWW-Authenticate': 'Bearer'},
#     #     )
        
#     # try:
#     #     user_id_uuid = uuid.UUID(user_id)
#     # except (TypeError, ValueError):
#     #     raise HTTPException(
#     #         status_code=status.HTTP_401_UNAUTHORIZED,
#     #         detail='Invalid or expired token',
#     #         headers={'WWW-Authenticate': 'Bearer'},
#     #     )
        
#     # result = await db.execute(
#     #     select(User).where(User.id == user_id_uuid),
#     # )
#     # user = result.scalars().first()
#     # if not user:
#     #     raise HTTPException(
#     #         status_code=status.HTTP_401_UNAUTHORIZED,
#     #         detail='User not found',
#     #         headers={'WWW-Authenticate': 'Bearer'},
#     #     )

#     # return user
#     ...


def require_role(*roles: Role):
    async def check(
        user: UserSchema = Depends(get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE))
    ):
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have rights for this action"
            )
        return user
    return check
