
from sqlmodel import SQLModel, Field, Relationship, ForeignKey
from uuid import uuid4
from datetime import datetime
from sqlalchemy.sql import func
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.patient.models import Patient

class Prediction(SQLModel, table=True):
    __tablename__ = "prediction"

    id: int = Field(default_factory=lambda: uuid4().int, primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    patient_id: int = Field(foreign_key="patient.id", nullable=False)
    timestamp: datetime = Field(sa_column_kwargs={"server_default": func.now()}, nullable=False)
    label: str
    probability: float

    # now we can reference Patient directly
    patient: Optional["Patient"] = Relationship(back_populates="predictions")


