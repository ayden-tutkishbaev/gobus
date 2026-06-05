import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from src.admin.permissions import require_role
from src.admin.schemas.routes import RouteCreate, RouteUpdate, RouteResponse, RouteListResponse
from src.auth.enum import Role
from src.dependencies import db_connection
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.routes.models import Route
from src.staff.models import Staff
from src.staff.enum import StaffRole
from src.auth.services import http_bearer


admin_route = APIRouter(
    dependencies=[
        Depends(http_bearer),
        Depends(require_role(Role.SUPERADMIN, Role.ADMIN)), 
    ]
)



@admin_route.post(
    path='/routes',
)
async def add_route(
    db: db_connection,
    route_data: RouteCreate,
):
    babysitter = await db.execute(select(Staff).where(Staff.id == route_data.babysitter_id))
    driver = await db.execute(select(Staff).where(Staff.id == route_data.driver_id))
    
    if not driver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Driver not found")
    
    if not not babysitter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Babysitter not found")
    
    if babysitter.scalars().first().staff_type != StaffRole.BABYSITTER or driver.scalars().first().staff_type != StaffRole.DRIVER:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incorrectly assigned role!")
    
    new_route = Route(
        name=route_data.name,
        estimated_duration_minutes=route_data.estimated_duration_minutes,
        driver_id=route_data.driver_id,
        babysitter_id=route_data.babysitter_id,
        transport_id=route_data.transport_id
    )
    
    
    db.add(new_route)
    await db.commit()
    await db.refresh(new_route)
    
    return new_route


@admin_route.patch(
    path="/routes/{route_id}",
)
async def edit_route(
    db: db_connection,
    data_edited: RouteUpdate, 
    route_id: uuid.UUID
):
    query = await db.execute(select(Route).where(Route.id == route_id))
    route = query.scalars().first()
    
    if not route:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Route not found')
    
    update_data = data_edited.model_dump(exclude_unset=True)
   
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No field to update")
   
    for field, value in update_data.items():
        setattr(route, field, value)
        
    await db.commit()
    await db.refresh(route)
    return route


@admin_route.get(
    path="/routes",
    response_model=list[RouteListResponse],
)
async def get_all_routes(
    db: db_connection,
    limit: int = 20,
    offset: int = 0
):
    result = await db.execute(select(Route).where(Route.is_active).limit(limit).offset(offset))
    return result.scalars().all()


@admin_route.get(
    path="/routes/{route_id}",
    response_model=RouteResponse,
)
async def get_route(
    route_id: uuid.UUID,
    db: db_connection, 
):
    result = await db.execute(select(Route).options(selectinload(Route.transport),
                                                                                selectinload(Route.babysitter),
                                                                                selectinload(Route.driver)).where(Route.id == route_id))
    route = result.scalars().first()
    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route not found"
        )
    return route


@admin_route.patch(
    path="/routes/{route_id}/deactivate",
)
async def deactivate_route(
    db: db_connection,
    route_id: uuid.UUID
):
    result = await db.execute(select(Route).where(Route.id == route_id))
    route = result.scalars().first()
    
    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            path="Parent not found"
        )
        
    route.is_active = False
    await db.commit()
    return {"detail": "Route has been deactivated"}