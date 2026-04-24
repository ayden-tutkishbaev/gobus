from fastapi import Depends, HTTPException, status
from typing import Annotated

from api.auth.models import User
from api.auth.utils import get_current_user



async def get_admin(
    user: Annotated[User, Depends(get_current_user)]
) -> User:
    if not user.is_superadmin and not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You do not have rights for this action!',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    return user


async def get_super_admin(
    user: Annotated[User, Depends(get_current_user)]
) -> User:
    if not user.is_superadmin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You do not have rights for this action!',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    return user