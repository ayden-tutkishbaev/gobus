import datetime
import uuid

from src.routes.enum import Status
from src.schema import AppBaseModel
from src.trips.enum import RouteStatus



class TransportModel(AppBaseModel):
    id: uuid.UUID
    unique_transport_id: str
    model: str
    status: Status
    

class StaffModel(AppBaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    phone_number: str


class RouteListResponse(AppBaseModel):
    id: uuid.UUID
    name: str
    is_active: bool
    driver: StaffModel | None = None
    babysitter: StaffModel | None = None


class RouteDetails(AppBaseModel):
    id: uuid.UUID
    name: str
    is_active: bool
    driver: StaffModel | None = None
    babysitter: StaffModel | None = None
    transport: TransportModel | None = None
    
    
class KidModel(AppBaseModel):
    id: uuid.UUID
    last_name: str
    first_name: str
    profile_photo_url: str | None = None
    phone_number: str | None = None
    home_address: str
    
    
class KidsListRoute(AppBaseModel):
    kids: list[KidModel] = []