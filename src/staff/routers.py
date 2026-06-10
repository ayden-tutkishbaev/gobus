from fastapi import APIRouter, Depends

from src.admin.permissions import require_role
from src.staff.babysitter.router import babysitter_router
from src.staff.driver.router import driver_router

from src.auth.services import http_bearer
from src.auth.enum import Role
from src.admin.permissions import require_role


staff_routers = [
    babysitter_router,
    driver_router
]

staff_router = APIRouter(
    prefix="/staff", 
    tags=['Staff'],
    # dependencies=[
    #     Depends(http_bearer),
    #     Depends(require_role(Role.BABYSITTER, Role.DRIVER)), 
    # ],
)

for router in staff_routers:
    staff_router.include_router(router)
    
    
@staff_router.get(path="/profile")
async def staff_profile():
    ...