from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import date
from sqlalchemy import Column, Text

if TYPE_CHECKING:
    from app.predict.models import Prediction

class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    date_of_birth: date
    email: Optional[str] = Field(default=None, index=True)
    phone: Optional[str] = None
    notes: Optional[str] = None

     # free‐form TEXT column for symptoms
    symptoms: Optional[str] = Field(
        default=None,
        sa_column=Column("symptoms", Text, nullable=True),
    )
    
    predictions:  List["Prediction"] = Relationship(back_populates="patient")
