#business logic around suers and tokens 

from datetime import datetime, timedelta, timezone
from uuid import uuid4

from passlib.context import CryptContext
from jose import jwt
from sqlmodel import Session, select

from app.database import engine
from app.auth.models import User, BlacklistedToken
from app.config import settings

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

#fetch a suer by username 
def get_user(username: str) -> User | None:
    with Session(engine) as sess:
        return sess.exec(select(User).where(User.username == username)).first()
    
#hash the plain password 
def create_user(username: str, email: str, password: str) -> User:
    user = User(
        username=username,
        email=email,
        hashed_password=pwd_ctx.hash(password)
    )
    with Session(engine) as sess:
        sess.add(user)
        sess.commit()
        sess.refresh(user)
    return user

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