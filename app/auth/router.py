#HTTP endpoints under /auth 
from jose import JWTError
from fastapi import APIRouter, Depends, HTTPException, status, Body, BackgroundTasks, Query 
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from app.auth.schemas import Token
from app.auth.service import revoke_token
from app.auth.dependencies import get_current_admin
from app.auth.service import get_user_by_email
from app.auth.service import send_verification_email, mark_user_verified
from app.config import settings
from app.auth.models import User, BlacklistedToken
from sqlmodel import Session, select
from app.database import engine
from app.auth import service
from app.auth import service as auth_svc, schemas, dependencies
from app.auth.dependencies import oauth2_scheme, get_current_user
from app.auth.schemas import LoginIn, TokenOut, RefreshIn   
from app.auth.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_jti,
)

router = APIRouter(tags=["auth"])

@router.post("/register", response_model=schemas.UserRead, status_code=201, summary="Register a new user")
def register(
    user_in: schemas.UserCreate,
    background_tasks: BackgroundTasks
    ):
    if service.get_user(user_in.username):
        raise HTTPException(400, "Username already registered")
    user = service.create_user(user_in.username, user_in.email, user_in.password)
    
    # schedule the “please verify” email
    background_tasks.add_task(service.send_verification_email, user.email)
    
    return user

@router.post(
    "/verify/resend",
    status_code=status.HTTP_200_OK,
    summary="Resend email verification link",
)
def resend_verification(email: str = Body(..., embed=True)):
    """
    Generates a short-lived 'email_verify' JWT and STUB-sends it by logging.
    """
    user = service.get_user_by_email(email)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Email not registered")
    if user.is_verified:
        return {"message": "Email already verified"}

    token = send_verification_email(email)
    return {"message": "Verification email sent", "token": token}

@router.get(
    "/verify-email",
    status_code=status.HTTP_200_OK,
    summary="Verify email via token link",
)
def verify_email(token: str = Query(..., description="Email verify JWT")):
    """
    User submits the token they received; we decode & flip `is_verified`.
    """
    try:
        email = service.verify_email_token(token)
    except JWTError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")

    user = service.mark_user_verified(email)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

    return {"message": "Email successfully verified"}

@router.post("/token", response_model=Token, summary="Get JWT access token")

@router.post("/login", response_model=TokenOut, summary="Get JWT access & refresh tokens")
def login(data: LoginIn):
    user = auth_svc.authenticate(data.username, data.password)
    if not user:
        raise HTTPException(401, "Invalid credentials")
    
    #unverified users 
    if not user.is_verified:
        raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Please verify your email before logging in."
    )
    access  = create_access_token(subject=str(user.id))
    refresh = create_refresh_token(subject=str(user.id))

    # Persist the refresh‐token’s JTI 
    # auth_svc.save_refresh_jti(user.id, refresh)

    return {
        "access_token":  access,
        "refresh_token": refresh,
        "token_type":    "bearer",
    }

@router.get("/me", response_model=schemas.UserRead, summary="Get the current authenticated user")
def read_current_user(current_user = Depends(dependencies.get_current_user)):
    return current_user

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT, summary="Revoke current JWT")
def logout(token: str = Depends(oauth2_scheme), current_user=Depends(get_current_user)):
    """
    Blacklist the currently used token so it cannot be reused.
    """
    # decode only to extract jti
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM], options={"verify_exp": False})
        jti = payload.get("jti")
        if not jti:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Malformed token")
    except jwt.PyJWTError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid token")

    # blacklist
    revoke_token(jti)
    return  # 204 No Content

@router.post("/refresh", response_model=TokenOut, summary="Rotate refresh token")
def refresh_endpoint(payload: RefreshIn):
    from app.auth.security import decode_token

    # decode & validate
    try:
        claims = decode_token(payload.refresh_token)
    except JWTError:
        raise HTTPException(401, "Invalid refresh token")

    # must be a refresh‐token
    if claims.get("type") != "refresh":
        raise HTTPException(400, "Invalid token type")

    old_jti = get_jti(claims)
    
    # revoke the old one
    if auth_svc.is_jti_blacklisted(old_jti):
        raise HTTPException(401, "Token already used")

    auth_svc.blacklist_jti(old_jti)

    # issue a fresh pair
    user_id = int(claims["sub"])
    new_access  = create_access_token(subject=str(user_id))
    new_refresh = create_refresh_token(subject=str(user_id))

    # persist the new refresh JTI
    auth_svc.save_refresh_jti(user_id, new_refresh)

    return {
        "access_token":  new_access,
        "refresh_token": new_refresh,
        "token_type":    "bearer",
    }
