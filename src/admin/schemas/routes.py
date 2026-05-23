import uuid

from pydantic import Field, model_validator

from src.schema import AppBaseModel
from src.routes.enum import Status

        
        
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



class RouteBase(AppBaseModel):
    name: str = Field(min_length=1, max_length=240)
    estimated_duration_minutes: int = Field(gt=0)
    

class RouteCreate(RouteBase):
    driver_id: uuid.UUID | None = None       
    babysitter_id: uuid.UUID | None = None   
    transport_id: uuid.UUID | None = None    
    
    
    @model_validator(mode="before")
    def ids_difference_required(cls, values):
        if values.get("babysitter_id") == values.get("driver_id"):
            raise ValueError("Babysitter and driver cannot be a single person!")
        return values
    
    
class RouteUpdate(AppBaseModel):
    name: str | None = None
    estimated_duration_minutes: int | None = None
    driver_id: uuid.UUID | None = None
    babysitter_id: uuid.UUID | None = None
    transport_id: uuid.UUID | None = None
    


class RouteListResponse(RouteBase):
    id: uuid.UUID
    is_active: bool
    driver_id: uuid.UUID | None = None
    babysitter_id: uuid.UUID | None = None
    transport_id: uuid.UUID | None = None


class RouteResponse(RouteBase):
    id: uuid.UUID
    is_active: bool
    driver: StaffModel | None = None      
    babysitter: StaffModel | None = None  
    transport: TransportModel | None = None