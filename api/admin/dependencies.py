from fastapi import Depends
from typing import Annotated
from api.auth.models import User
from api.admin.filters import get_admin, get_super_admin


IsAdmin = Annotated[User, Depends(get_admin)]
IsSuperAdmin = Annotated[User, Depends(get_super_admin)]