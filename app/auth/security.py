# pure JWT logic 
import uuid
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from typing import Dict

from app.config import settings

ALGORITHM = settings.ALGORITHM
SECRET_KEY = settings.SECRET_KEY

# lifetimes
ACCESS_TOKEN_EXPIRE_MINUTES  = settings.ACCESS_TOKEN_EXPIRE_MINUTES  # 60
REFRESH_TOKEN_EXPIRE_DAYS    = 7

def create_access_token(subject: str) -> str:
    now = datetime.now(timezone.utc)
    jti = str(uuid.uuid4())
    payload: Dict[str, any] = {
        "sub": subject,
        "jti": jti,
        "iat": now,
        "exp": now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "type": "access",
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(subject: str) -> str:
    now = datetime.now(timezone.utc)
    jti = str(uuid.uuid4())
    payload: Dict[str, any] = {
        "sub": subject,
        "jti": jti,
        "iat": now,
        "exp": now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        "type": "refresh",
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> Dict[str, any]:
    # will raise JWTError on invalid/expired
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

def get_jti(claims: Dict[str, any]) -> str:
    return claims["jti"]
