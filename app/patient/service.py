from sqlmodel import Session, select
from fastapi import HTTPException
from sqlalchemy.orm import selectinload

from app.database import engine
from app.patient.models import Patient
from app.patient.schemas import PatientCreate, PatientUpdate


def create_patient(data: PatientCreate) -> Patient:
    payload = data.model_dump()
    # convert list of symptoms into comma-separated string
    payload["symptoms"] = ", ".join(payload.get("symptoms", []) or [])

    patient = Patient(**payload)
    with Session(engine) as sess:
        sess.add(patient)
        sess.commit()
        sess.refresh(patient)
        return patient


def get_patient(patient_id: int) -> Patient | None:
    with Session(engine) as sess:
        stmt = (
            select(Patient)
            .where(Patient.id == patient_id)
            .options(selectinload(Patient.predictions))
        )
        return sess.exec(stmt).first()


def list_patients(skip: int = 0, limit: int = 100) -> list[Patient]:
    with Session(engine) as sess:
        stmt = (
            select(Patient)
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
        return patient


def delete_patient(patient_id: int) -> None:
    with Session(engine) as sess:
        patient = sess.get(Patient, patient_id)
        if patient:
            sess.delete(patient)
            sess.commit()

