from pydantic import BaseModel, ConfigDict, Field
import uuid
from src.auth.enum import UserRole


class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    phone_number: str
    
    
class UserCreate(UserBase):
    password: str = Field(min_length=1)
    role: UserRole


    
class UserPublic(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    username: str
    

class UserPrivate(UserPublic):
    username: str
    
    
class Token(BaseModel):
    access_token: str
    token_type: str
        
