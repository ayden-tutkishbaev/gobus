import uuid

from pydantic import Field

from datetime import datetime
from src.routes.enum import Status
from typing import Optional
from src.schema import AppBaseModel

    
class TransportBase(AppBaseModel):
    unique_transport_id: str = Field(min_length=1, max_length=90)
    model: str = Field(min_length=1, max_length=90)
    
    
class TransportCreate(TransportBase): 
    capacity: int = Field(gt=0)
    status: Status = Status.ACTIVE
    

class TransportResponse(TransportBase):
    id: uuid.UUID
    registered_at: datetime
    photo_url: str | None = None
    capacity: int
    status: Status
    
    
class TransportUpdate(AppBaseModel):
    unique_transport_id: str = Field(default=None, min_length=1, max_length=90)
    model: Optional[str] = None
    capacity: Optional[str] = None
    status: Optional[Status] = None