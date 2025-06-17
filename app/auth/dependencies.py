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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token") #reads authorization header 

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
   
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM], options={"require": ["sub", "exp", "jti", "iat"]})
        username: str = payload.get("sub")
        jti = payload.get("jti")
        if not username or not jti:
            raise JWTError("Missing sub or jti claims")
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
            select(User).where(User.username == username)
        ).one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

    return user