import uuid

from pydantic import Field

from src.schema import AppBaseModel

from datetime import datetime
from typing import Optional
        
        
    
class SchoolBase(AppBaseModel):
    name: str = Field(min_length=1, max_length=260)
    address: str
    

class SchoolCreate(SchoolBase):
    geo_latitude: float
    geo_longitude: float  
    
    
class SchoolResponse(SchoolBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    
    
class SchoolUpdate(AppBaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=260)
    address: Optional[str] = None
    geo_latitude: Optional[float] = None
    geo_longitude: Optional[float] = None  