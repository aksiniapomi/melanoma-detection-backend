# app/auth/router.py
#from fastapi import APIRouter
#router = APIRouter()
#@router.get("/ping")
#def ping():
 #   return {"pong": True}

#HTTP endpoints under /auth 

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import service, schemas, dependencies

router = APIRouter()

@router.post("/register", response_model=schemas.UserRead, status_code=201)
def register(user_in: schemas.UserCreate):
    if service.get_user(user_in.username):
        raise HTTPException(400, "Username already registered")
    user = service.create_user(user_in.username, user_in.email, user_in.password)
    return user

@router.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = service.get_user(form_data.username)
    if not user or not service.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    token = service.create_access_token(user.username)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserRead)
def read_current_user(current_user = Depends(dependencies.get_current_user)):
    return current_user
