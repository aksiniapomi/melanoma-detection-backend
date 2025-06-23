from sqlmodel import SQLModel, Field 
from typing import Optional, List
from datetime import date

class PatientCreate(SQLModel):
    first_name: str
    last_name: str
    date_of_birth: date
    email: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None
    symptoms: Optional[List[str]] = Field(default=[])

class PatientRead(PatientCreate):
    id: int

class PatientUpdate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None
    symptoms: Optional[List[str]] = None
