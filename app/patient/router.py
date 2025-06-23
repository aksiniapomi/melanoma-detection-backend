from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.dependencies import get_current_user
from app.patient import service, schemas
from typing import List

router = APIRouter(
    prefix="/patients",
    tags=["patients"],
    dependencies=[Depends(get_current_user)],  # only logged-in users
)

@router.post("/", response_model=schemas.PatientRead, status_code=status.HTTP_201_CREATED)
def create_patient(data: schemas.PatientCreate):
    return service.create_patient(data)

@router.get("/", response_model=list[schemas.PatientRead])
def read_patients(skip: int = 0, limit: int = 100):
    return service.list_patients(skip, limit)

@router.get("/{patient_id}", response_model=schemas.PatientRead)
def read_patient(patient_id: int):
    patient = service.get_patient(patient_id)
    if not patient:
        raise HTTPException(404, "Patient not found")
    return patient

@router.patch("/{patient_id}", response_model=schemas.PatientRead)
def patch_patient(patient_id: int, changes: schemas.PatientUpdate):
    patient = service.get_patient(patient_id)
    if not patient:
        raise HTTPException(404, "Patient not found")
    return service.update_patient(patient_id, changes.model_dump(exclude_none=True))

@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int):
    service.delete_patient(patient_id)
