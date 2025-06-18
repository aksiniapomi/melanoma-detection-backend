
#HTTP endpoints under /auth 

from fastapi import APIRouter, Depends, HTTPException, status, Body 
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from app.auth import service, schemas, dependencies
from app.auth.schemas import Token
from app.auth.dependencies import oauth2_scheme
from app.auth.service import revoke_token
from app.auth.dependencies import get_current_user
from app.auth.service import get_user_by_email, create_email_token
from app.utils.email import send_email
from app.auth.service import send_verification_email, verify_email_token, mark_user_verified
from app.config import settings
from app.auth.models import User, BlacklistedToken

router = APIRouter()

@router.post("/register", response_model=schemas.UserRead, status_code=201, summary="Register a new user")
def register(user_in: schemas.UserCreate):
    if service.get_user(user_in.username):
        raise HTTPException(400, "Username already registered")
    user = service.create_user(user_in.username, user_in.email, user_in.password)
    return user

@router.post(
    "/verify/send",
    status_code=status.HTTP_200_OK,
    summary="Send a one-time email verification link/token",
)
def send_verification(email: str = Body(..., embed=True)):
    """
    Generates a short-lived 'email_verify' JWT and STUB-sends it by logging.
    """
    user = service.get_user_by_email(email)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Email not registered")
    if user.is_verified:
        return {"message": "Email already verified"}

    token = send_verification_email(email)
    return {"message": "Verification email sent (stubbed)", "token": token}

@router.post(
    "/verify",
    status_code=status.HTTP_200_OK,
    summary="Consume a verification token and mark email as verified",
)
def verify_email(token: str = Body(..., embed=True)):
    """
    User submits the token they received; we decode & flip `is_verified`.
    """
    try:
        email = service.verify_email_token(token)
    except Exception:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")

    user = service.mark_user_verified(email)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

    return {"message": "Email successfully verified"}

@router.post("/token", response_model=Token, summary="Get JWT access token")
@router.post("/login", response_model=Token, summary="Get JWT access token (alias)")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = service.get_user(form_data.username)
    if not user or not service.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = service.create_access_token(subject=user.username)
    return {"access_token": token, "token_type": "bearer"}

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