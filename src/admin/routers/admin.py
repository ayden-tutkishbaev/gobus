from fastapi import APIRouter

from src.admin.routers.kids import admin_kid
from src.admin.routers.contracts import admin_contract
from src.admin.routers.parents import admin_parent
from src.admin.routers.routes import admin_route
from src.admin.routers.schools import admin_school
from src.admin.routers.staff import admin_staff
from src.admin.routers.teachers import admin_teacher
from src.admin.routers.transport import admin_transport

admin_routers = [
    admin_kid,
    admin_contract,
    admin_parent,
    admin_route,
    admin_school,
    admin_staff,
    admin_teacher,
    admin_transport,
]

admin_router = APIRouter(prefix="/admin", tags=['Admins'])

for router in admin_routers:
    admin_router.include_router(router)