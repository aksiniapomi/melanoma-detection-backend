from sqlmodel import Session, select
from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from app.database import engine
from app.patient.models import Patient
from app.patient.schemas import PatientCreate, PatientUpdate

def create_patient(data: PatientCreate, owner_id: int) -> Patient:
    payload = data.model_dump()
    #build flat payload from the Pydantic model 
    payload["owner_id"] = owner_id
    # convert list of symptoms into comma-separated string
    payload["symptoms"] = ", ".join(payload.get("symptoms", []) or [])
    
    #check for an existing patient; check and create in the same session 
    with Session(engine) as sess:
        dup = sess.exec(
            select(Patient)
            #.where(Patient.owner_id     == owner_id) to block duplucates gloablly without owner id 
            .where(Patient.first_name   == payload["first_name"])
            .where(Patient.last_name    == payload["last_name"])
            .where(Patient.date_of_birth== payload["date_of_birth"])
        ).first()
        if dup:
            raise HTTPException(
                status_code=400,
                detail="A patient with that name and date of birth already exists."
            )

    #in case of no duplicate, create 
    patient = Patient(**payload)
    sess.add(patient)
    sess.commit()
    sess.refresh(patient)
    return get_patient(patient.id)


def get_patient(patient_id: int) -> Patient | None:
    with Session(engine) as sess:
        stmt = (
            select(Patient)
            .where(Patient.id == patient_id)
            .options(selectinload(Patient.predictions))
        )
        return sess.exec(stmt).first()

def list_patients(skip: int = 0, limit: int = 100) -> list[Patient]:
    
    # List all patients (for admins)
    with Session(engine) as sess:
        stmt = (
            select(Patient)
            .options(selectinload(Patient.predictions))
            .offset(skip)
            .limit(limit)
        )
        return sess.exec(stmt).all()


def list_patients_for_owner(owner_id: int, skip: int = 0, limit: int = 100) -> list[Patient]:
    
    #List only patients belonging to a specific owner.
    with Session(engine) as sess:
        stmt = (
            select(Patient)
            .where(Patient.owner_id == owner_id)
            .options(selectinload(Patient.predictions))
            .offset(skip)
            .limit(limit)
        )
        return sess.exec(stmt).all()

def update_patient(patient_id: int, changes: dict) -> Patient:
    # if updating symptoms, convert list to comma-separated string
    if "symptoms" in changes:
        changes["symptoms"] = ", ".join(changes.get("symptoms", []) or [])

    with Session(engine) as sess:
        patient = sess.get(Patient, patient_id)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")

        for field, value in changes.items():
            setattr(patient, field, value)

        sess.add(patient)
        sess.commit()
        sess.refresh(patient)
        return get_patient(patient_id)


def delete_patient(patient_id: int) -> None:
    with Session(engine) as sess:
        patient = sess.get(Patient, patient_id)
        if patient:
            sess.delete(patient)
            sess.commit()

