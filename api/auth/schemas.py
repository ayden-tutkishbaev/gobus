from pydantic import BaseModel, ConfigDict, Field
from database.enum import Role
import uuid
from datetime import datetime
    

class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    
    
class UserCreate(UserBase):
    password: str = Field(min_length=1)
    #date


    
class UserPublic(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    username: str
    

class UserPrivate(UserPublic):
    username: str
    
    
class Token(BaseModel):
    access_token: str
    token_type: str
        
