import uuid

from pydantic import Field

from datetime import datetime
from typing import Optional
from src.schema import AppBaseModel


class ParentBase(AppBaseModel):
    last_name: str = Field(min_length=1, max_length=260)
    first_name: str = Field(min_length=1, max_length=260)
    middle_name: str = Field(min_length=1, max_length=260)
    phone_number: str
    

class ParentCreate(ParentBase):
    document_id: str = Field(min_length=5, max_length=90)
    home_address: str = Field(min_length=1, max_length=260)
    
    
class ParentResponse(ParentBase):
    id: uuid.UUID
    is_active: bool
    registered_at: datetime
    home_address: str = Field(min_length=1, max_length=260)
    profile_photo_url: str | None = None
    
    
    
class ParentUpdate(AppBaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    document_id: Optional[str] = None
    active: Optional[bool] = None