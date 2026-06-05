from pydantic import BaseModel, ConfigDict, Field
import uuid
from src.auth.enum import UserRole, Role
from src.schema import AppBaseModel


class UserBase(AppBaseModel):
    username: str = Field(min_length=1, max_length=50)
    phone_number: str
    
    
class UserCreate(UserBase):
    password: str = Field(min_length=1)
    role: UserRole


    
# class UserPublic(UserBase):
#     model_config = ConfigDict(from_attributes=True)
    
#     id: uuid.UUID
#     username: str
    

# class UserPrivate(UserPublic):
#     username: str
    
    
# class Token(BaseModel):
#     access_token: str
#     token_type: str
        


class UserSchema(AppBaseModel):
    id: uuid.UUID
    username: str
    role: Role
    phone_number: str
    
    
#TODO: add necessary fields
    
    
class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
    