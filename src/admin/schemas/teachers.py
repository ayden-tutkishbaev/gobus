from datetime import datetime
import uuid

from pydantic import Field

from src.schema import AppBaseModel 
            
    
class TeacherBase(AppBaseModel):
    last_name: str = Field(min_length=1, max_length=260)
    first_name: str = Field(min_length=1, max_length=260)
    middle_name: str = Field(min_length=1, max_length=260)
    phone_number: str
    
    
class TeacherCreate(TeacherBase):
    school_id: uuid.UUID  
    
    
class TeacherUpdate(AppBaseModel):
    last_name: str | None = Field(None, min_length=1, max_length=260)
    first_name: str | None = Field(None, min_length=1, max_length=260)
    middle_name: str | None = Field(None, min_length=1, max_length=260)
    phone_number: str | None = None
    school_id: uuid.UUID | None = None
    
    
class SchoolModel(AppBaseModel):
    name: str
    address: str
    
    
class TeacherListResponse(TeacherBase):
    id: uuid.UUID
    is_active: bool
    registered_at: datetime
    school_id: uuid.UUID


class TeacherResponse(TeacherBase):
    id: uuid.UUID   
    is_active: bool
    registered_at: datetime
    school: SchoolModel | None = None
    
    