from sqlmodel import SQLModel, Field, Relationship
from datetime import date
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Column, Text

if TYPE_CHECKING:
    from app.predict.models import Prediction

class Patient(SQLModel, table=True):
    __tablename__ = "patient"

    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    date_of_birth: date
    email: Optional[str] = Field(default=None, index=True)
    phone: Optional[str] = None
    notes: Optional[str] = None
    symptoms: Optional[str] = Field(
        sa_column=Column("symptoms", Text, nullable=True),
        default=None,
    )

    predictions: List["Prediction"] = Relationship(back_populates="patient")
