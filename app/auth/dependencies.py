#dependency functions for protected endpoints 

from datetime import datetime, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, ExpiredSignatureError
from sqlmodel import Session, select
from jose import jwt

from app.config import settings
from app.database import engine
from app.auth.models import User, BlacklistedToken
from app.auth.schemas import Token
from app.auth import service as auth_svc

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token") #reads authorization header 

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"require": ["sub", "exp", "jti", "iat"]}
        )
        # our sub claim is the user ID, so parse it
        sub = int(payload.get("sub"))
        jti = payload.get("jti")
        if sub is None or jti is None:
            raise JWTError("Missing sub or jti claims")
        # sub is user ID
        user_id = int(sub)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Expired token", 
            headers={"WWW-Authenticate": "Bearer"})
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    #blacklisted token check 
    with Session(engine) as sess:
        blacklisted = sess.exec(
            select(BlacklistedToken).where(BlacklistedToken.jti == jti)
        ).first()
        if blacklisted:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # fetch user
    with Session(engine) as sess:
        user = sess.exec(
            select(User).where(User.id == user_id)
        ).one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
    return user

async def get_current_admin(user=Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return user