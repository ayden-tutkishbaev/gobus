from fastapi import APIRouter, HTTPException, status, Depends
from src.dependencies import db_connection
from src.auth.services import http_bearer
from src.auth.enum import Role
from src.admin.permissions import require_role


driver_router = APIRouter(
    prefix="/driver",
    dependencies=[
        Depends(http_bearer),
        Depends(require_role(Role.DRIVER)), 
    ],
    
)


@driver_router.get(path="/test-endpoint")
async def test():
    return "Hey"