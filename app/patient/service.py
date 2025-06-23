import json
from sqlmodel import Session, select
from app.database import engine
from app.patient import schemas
from app.patient.models import Patient
from app.patient.schemas import PatientCreate

def create_patient(data: PatientCreate) -> Patient:
    payload = data.model_dump()
    # turn the Python list into a JSON string
    payload["symptoms"] = json.dumps(payload.get("symptoms", []))
    patient = Patient(**payload)
    with Session(engine) as sess:
        sess.add(patient)
        sess.commit()
        sess.refresh(patient)
        patient.symptoms = json.loads(patient.symptoms or "[]")
        return patient

def get_patient(patient_id: int) -> Patient | None:
    with Session(engine) as sess:
        patient = sess.get(Patient, patient_id)
        if patient:
            patient.symptoms = json.loads(patient.symptoms or "[]")
        return patient

def list_patients(skip: int = 0, limit: int = 100) -> list[Patient]:
    with Session(engine) as sess:
        patients = sess.exec(select(Patient).offset(skip).limit(limit)).all()
    for p in patients:
        p.symptoms = json.loads(p.symptoms or "[]")
    return patients

def update_patient(patient_id: int, changes: dict) -> Patient:
    # serialize incoming list
    if "symptoms" in changes:
        changes["symptoms"] = json.dumps(changes["symptoms"] or [])
    with Session(engine) as sess:
        patient = sess.get(Patient, patient_id)
        for k, v in changes.items():
            setattr(patient, k, v)
        sess.add(patient)
        sess.commit()
        sess.refresh(patient)
        # _deserialize_ for the response
        patient.symptoms = json.loads(patient.symptoms or "[]")
        return patient

def delete_patient(patient_id: int) -> None:
    with Session(engine) as sess:
        patient = sess.get(Patient, patient_id)
        sess.delete(patient)
        sess.commit()
