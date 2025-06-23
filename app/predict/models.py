
from sqlmodel import SQLModel, Field, ForeignKey
from uuid import uuid4
from datetime import datetime
from sqlalchemy.sql import func

class Prediction(SQLModel, table=True):
    id: int = Field(default_factory=lambda: uuid4().int, primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    timestamp: datetime = Field(sa_column_kwargs={"server_default": func.now()}, nullable=False)
    label: str
    probability: float

