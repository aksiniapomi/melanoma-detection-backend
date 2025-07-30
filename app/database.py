#sets up SQLModel/SQLAlchemy engine and table creation 

from sqlmodel import SQLModel, create_engine
from app.config import settings #import settings instance to see which database to use 
import app.models

engine = create_engine(
    settings.DATABASE_URL,
    echo=True,               # set False in production; show every sql statement in the console 
    connect_args={"check_same_thread": False}  # only for SQLite
)

def init_db():
    SQLModel.metadata.create_all(engine)
