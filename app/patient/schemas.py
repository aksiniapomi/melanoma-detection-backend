from sqlmodel import SQLModel, Field 
from pydantic import EmailStr, field_validator
from typing import Optional, List
from datetime import date
from app.predict.schemas import PredictionOut
from sqlmodel import SQLModel

class PatientCreate(SQLModel):
    first_name: str = Field(..., max_length=50)
    last_name:  str = Field(..., max_length=50)
    date_of_birth: date
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, max_length=20)
    notes: Optional[str] = Field(default=None, max_length=500)
    symptoms: List[str] = Field(default=[], min_items=0, max_items=10) #capped to 10 symptoms per patient 
    
    @field_validator("date_of_birth")
    def dob_not_future_and_not_too_old(cls, v: date) -> date:
        today = date.today()
        if v > today:
            raise ValueError("DOB cannot be in the future")
        if v < date(today.year - 120, today.month, today.day):
            raise ValueError("date_of_birth implausibly far in the past")
        return v

    @field_validator("symptoms")
    def validate_symptoms(cls, v: List[str]) -> List[str]:
        if not isinstance(v, list):
            raise ValueError("symptoms must be a list of strings")
        if len(v) > 10:
            raise ValueError("no more than 10 symptoms allowed")
        cleaned = []
        for s in v:
            if not isinstance(s, str):
                raise ValueError("each symptom must be a string")
            s2 = s.strip()
            if not s2:
                raise ValueError("each symptom must be a non-empty string")
            if len(s2) > 100:
                raise ValueError("individual symptom too long")
            cleaned.append(s2)
        return cleaned

class PatientRead(SQLModel):
    id: int
    first_name: str
    last_name: str
    date_of_birth: date
    email: Optional[str]
    phone: Optional[str]
    notes: Optional[str]
    symptoms: Optional[str]

    # pull in the list of predictions
    predictions: List["PredictionOut"] = []

class PatientUpdate(SQLModel):
    first_name: Optional[str] = Field(default=None, max_length=50)
    last_name:  Optional[str] = Field(default=None, max_length=50)
    date_of_birth: Optional[date] = None
    email: Optional[EmailStr]     = None
    phone: Optional[str]     = Field(default=None, max_length=20)
    notes: Optional[str]     = Field(default=None, max_length=500)
    symptoms: Optional[List[str]] = Field(default=None, min_items=0, max_items=10)

