import uuid

from fastapi import Depends
from src.auth.schemas import UserSchema
from src.auth.services import ACCESS_TOKEN_TYPE, get_auth_user_from_token_of_type
from src.dependencies import db_connection
from src.routes.models import babysitter_router
from src.trips.models import Trip
from src.trips.enum import RouteStatus


@babysitter_router.post(
    path="/trips/{route_id}/start"
)
async def start_trip(
    db: db_connection,
    route_id: uuid.UUID
):
    new_trip = Trip(
        route_id=route_id,
        status=RouteStatus.IN_PROGRESS,
    )
    
    # attendance по каждому ребёнку создать
    
    db.add(new_trip)
    await db.commit()
    
    return {"detail": "Trip started!"}


@babysitter_router.get(
    
)
async def get_all_trips(
    
):
    ...
    
    
@babysitter_router.get(
    
)
async def get_trip(
    
):
    ...
    # trip_id
    
    #attendance списком