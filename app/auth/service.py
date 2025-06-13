#business logic around suers and tokens 

from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from sqlmodel import Session, select

from app.database import engine
from app.auth.models import User
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
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
