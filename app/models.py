from datetime import datetime, timezone 
from typing import Optional

from sqlmodel import SQLModel, Field

class Prediction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="UTC timestamp when the prediction was created")
    label: str
    probability: float
