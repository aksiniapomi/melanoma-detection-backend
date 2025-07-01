from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.dependencies import get_current_user
from app.patient import service, schemas
from typing import List

router = APIRouter(
    tags=["patients"],
    dependencies=[Depends(get_current_user)],   #Require login for all patient routes
)

@router.post("/", response_model=schemas.PatientRead, status_code=status.HTTP_201_CREATED)
def create_patient(
    data: schemas.PatientCreate,
    current_user = Depends(get_current_user),
):
    #Create a new patient owned by the current user
    return service.create_patient(data, owner_id=current_user.id)

@router.get("/", response_model=List[schemas.PatientRead])
def read_patients(
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_user),
):
    
    #List patients: all if admin, else only those owned by the user
    
    if current_user.is_admin:
        return service.list_patients(skip, limit)
    return service.list_patients_for_owner(current_user.id, skip, limit)

@router.get("/{patient_id}", response_model=schemas.PatientRead)
def read_patient(
    patient_id: int,
    current_user = Depends(get_current_user),
):
    #Fetch a single patient, enforcing owner/admin permissions
    
    patient = service.get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    if not current_user.is_admin and patient.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this patient")
    return patient

@router.patch("/{patient_id}", response_model=schemas.PatientRead)
def patch_patient(
    patient_id: int,
    changes: schemas.PatientUpdate,
    current_user = Depends(get_current_user),
):
    #Update a patient, enforcing owner/admin permissions
    
    patient = service.get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    if not current_user.is_admin and patient.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this patient")
    return service.update_patient(patient_id, changes.model_dump(exclude_none=True))

@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(
    patient_id: int,
    current_user = Depends(get_current_user),
):
    
    #Delete a patient, enforcing owner/admin permissions
    
    patient = service.get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    if not current_user.is_admin and patient.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this patient")
    service.delete_patient(patient_id)


