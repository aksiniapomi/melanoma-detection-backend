#request bodies and responses 
#decouple internal database schema from what the api exposes 

from pydantic import BaseModel

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
