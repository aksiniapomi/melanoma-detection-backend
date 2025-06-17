
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Prediction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    label: str
    probability: float
