from pydantic import BaseModel, ConfigDict, Field
from database.options import Role
import uuid, datetime


    

class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    role: Role
    
    
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


# class SchoolBase(BaseModel):
#     name: str = Field(max_length=240)

# class SchoolCreate(SchoolBase):
#     pass

# class SchoolRead(SchoolBase):
#     model_config = ConfigDict(from_attributes=True)
#     id: int
    