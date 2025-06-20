#business logic around users and tokens 

import logging
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from passlib.context import CryptContext
from jose import jwt, JWTError
from sqlmodel import Session, select

from app.database import engine
from app.auth.models import User, BlacklistedToken
from app.config import settings
from app.utils.email  import send_email
from app.auth.schemas import UserRead
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# helper to hash raw passwords
def hash_password(raw_password: str) -> str:
 return pwd_ctx.hash(raw_password)

#fetch a user by username 
def get_user(username: str) -> User | None:
    with Session(engine) as sess:
        return sess.exec(select(User).where(User.username == username)).first()
    
def create_user(username: str, email: str, password: str) -> UserRead:
  with Session(engine) as sess:
    user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password),
        is_verified=False,
    )
    sess.add(user)
    try:
            sess.commit()
            sess.refresh(user)
    except IntegrityError as e:
            sess.rollback()
            raise HTTPException(
                status_code=400,
                detail="A user with that username or email already exists.",
            )
    return UserRead.model_validate(user,from_attributes=True)

def get_user_by_email(email: str) -> User | None:
    with Session(engine) as sess:
        return sess.exec(select(User).where(User.email == email)).first()

def create_email_token(subject: str) -> str:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.EMAIL_TOKEN_EXPIRE_MINUTES)
    jti = str(uuid4())
    payload = {
        "sub": subject,
        "exp": expire,
        "iat": now,
        "jti": jti,
        "scope": "email_verify"
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

#check the password against the bcrypt hash 
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)

#build and sign jwt with sub=username and expiry 
def create_access_token(subject: str) -> str:
    """
    Builds and signs a JWT with:
      - sub=username
      - exp=now + expiry
      - jti=random UUID for revocation tracking
    """
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    jti = str(uuid4())
    to_encode = {
        "sub": subject,
        "exp": expire,
        "iat": now,
        "jti": jti
    }
    encoded = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded

def generate_email_verification_token(email: str) -> str:
    now    = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.EMAIL_TOKEN_EXPIRE_MINUTES)
    to_sign = {
        "sub":   email,
        "exp":   expire,
        "scope": "email_verify",
        "jti":   str(uuid4())
    }
    return jwt.encode(to_sign, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_email_token(token: str) -> str:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"require": ["exp","sub","scope"]}
        )
        if payload.get("scope") != "email_verify":
            raise JWTError("Wrong token scope")
        return payload["sub"]
    except JWTError as e:
        raise

def mark_user_verified(email: str) -> User:
    with Session(engine) as session:
        stmt = select(User).where(User.email == email)
        user = session.exec(stmt).one_or_none()
        if not user:
            return None
        user.is_verified = True
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

def send_verification_email(email: str):
    # generate the token 
    token = generate_email_verification_token(email)
    # refer to the token 
    link = f"{settings.FRONTEND_URL}/verify?token={token}"
    body = f"Click here to verify your address:\n\n{link}"
    # SendGrid call
    send_email(to=email, subject="Please verify your email", body=body)
    return token

def revoke_token(jti: str) -> BlacklistedToken:
    """
    Store a tokens jti in the blacklist so it can no longer be used
    """
    bl = BlacklistedToken(jti=jti)
    with Session(engine) as sess:
        sess.add(bl)
        sess.commit()
        sess.refresh(bl)
    return bl