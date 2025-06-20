#request bodies and responses 
#decouple internal database schema from what the api exposes 

from pydantic import BaseModel
from datetime import datetime

#input payload for registration 
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

#what we send back when we return user data 
class UserRead(BaseModel):
    id: int
    username: str
    email: str

#jwt response 
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
class UserAdminRead(BaseModel):
    id: int
    username: str
    email: str
    is_verified: bool
    is_admin: bool
    created_at: datetime

    model_config = {"from_attributes": True}

class UserAdminUpdate(BaseModel):
    is_verified: bool | None = None
    is_admin: bool | None = None
