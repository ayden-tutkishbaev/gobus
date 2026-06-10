import uuid

from fastapi import APIRouter, HTTPException, status, Depends
from src.auth.schemas import UserSchema
from src.auth.services import ACCESS_TOKEN_TYPE, get_auth_user_from_token_of_type
from src.dependencies import db_connection
from src.kids.models import Kid
from src.routes.models import Route
from src.auth.models import User
from src.staff.models import Staff
from src.staff.schemas import KidModel, KidsListRoute, RouteDetails, RouteListResponse, StaffModel, TransportModel

from sqlalchemy.orm import selectinload
from sqlalchemy import select, and_

from src.auth.services import http_bearer
from src.auth.enum import Role
from src.admin.permissions import require_role


babysitter_router = APIRouter(
    # dependencies=[
    #     Depends(http_bearer),
    #     Depends(require_role(Role.BABYSITTER)), 
    # ],
    prefix="/babysitter",
)


@babysitter_router.get(
    path="/routes",
    response_model=list[RouteListResponse]
)
async def get_all_routes(
    db: db_connection,
    current_user: UserSchema = Depends(get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)),
    limit: int = 20,    
    offset: int = 0
):
    print(current_user)
    result = await db.execute(
        select(Route)
        .options(
            selectinload(Route.transport),
            selectinload(Route.babysitter).selectinload(Staff.user),
            selectinload(Route.driver).selectinload(Staff.user),
        )
        .where(and_(Route.is_active == True, Route.babysitter_id == current_user.staff.id))
        .limit(limit)
        .offset(offset)
    )
    
    routes = result.scalars().all()
    def to_staff_model(staff: Staff | None):
        if staff is None:
            return None
        return StaffModel(
            id=staff.id,
            first_name=staff.first_name,
            last_name=staff.last_name,
            phone_number=staff.user.phone_number,
        )

    return [
        RouteListResponse(
            id=r.id,
            name=r.name,
            is_active=r.is_active,
            driver=to_staff_model(r.driver),
            babysitter=to_staff_model(r.babysitter),
        )
        for r in routes
    ]
    


@babysitter_router.get(
    path="/route/{route_id}",
    response_model=RouteDetails
)
async def get_route_details(
    route_id: uuid.UUID,
    db: db_connection
):
    result = await db.execute(
        select(Route)
        .options(
            selectinload(Route.transport),
            selectinload(Route.babysitter).selectinload(Staff.user),
            selectinload(Route.driver).selectinload(Staff.user),
        )
        .where(Route.id == route_id)
    )
    
    route = result.scalars().first()
    
    if route is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Route not found")
    
    def to_staff_model(staff: Staff | None):
        if staff is None:
            return None
        return StaffModel(
            id=staff.id,
            first_name=staff.first_name,
            last_name=staff.last_name,
            phone_number=staff.user.phone_number,
        )

    return RouteDetails(
        id=route.id,
        name=route.name,
        is_active=route.is_active,
        driver=to_staff_model(route.driver),
        babysitter=to_staff_model(route.babysitter),
        transport=TransportModel.model_validate(route.transport)
    )


@babysitter_router.get(
    path="/route/{route_id}/kids",
    response_model=KidsListRoute
)
async def get_route_details(
    route_id: uuid.UUID,
    db: db_connection
):
    result = await db.execute(
        select(Kid)
        .where(and_(Kid.route_id == route_id, Kid.is_active == True))
    )
    kids = result.scalars().all()
    
    return KidsListRoute(
        kids=[
            KidModel(
                id=kid.id,
                last_name=kid.last_name,
                first_name=kid.first_name,
                profile_photo_url=kid.profile_photo_url,
                phone_number=kid.phone_number,
                home_address=kid.home_address,
            )
            for kid in kids
        ]
    )
    


@babysitter_router.get(
    path="/route/kid/{kid_id}"
)
async def get_kid_details(
    kid_id: uuid.UUID,
    db: db_connection
):
    result = await db.execute(
        select(Kid)
        .options(
            selectinload(Kid.school),
            selectinload(Kid.route),
            selectinload(Kid.contract),
            selectinload(Kid.teacher),
            selectinload(Kid.parents),
        )
        .where(Kid.id == kid_id)
    )
    kid = result.scalar_one_or_none()
    
    if not kid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Kid not found")
        
    return kid