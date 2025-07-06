
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Query
from app.auth.dependencies import get_current_user
from app.predict.schemas import PredictionOut
from app.predict import service as predict_service
from pathlib import Path 
from typing import List 
from app.patient import service as patient_service
from app.auth.dependencies import get_current_user

ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".bmp"}
MAX_FILE_SIZE = 5 * 1024 * 1024   # 5 MB

router = APIRouter(
    prefix="/patients/{patient_id}/predictions",
    tags=["predictions"],
    dependencies=[Depends(get_current_user)],
)

@router.post("/", response_model=PredictionOut, summary="Upload image and get melanoma probability")

async def predict(
    patient_id: int,                             
    image: UploadFile = File(...),
    current_user=Depends(get_current_user) #only logged in users can call /predict 
):
    
    """
    Stub /predict endpoint.
    Accepts an image upload and returns a dummy melanoma probability.
    Persists each call to the sqlite database 
    """
    # verify file type
    ext = Path(image.filename).suffix.lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(400, f"Unsupported file extension {ext}. Please upload a valid image file")
  
    # Read bytes (real ML here later); enforce the file size 
    img_bytes = await image.read()
    if len(img_bytes) > MAX_FILE_SIZE:
        raise HTTPException(413, "File too large (max 5 MB)")
    #ML model goes here 

    # dummy inference 
    prob = 0.42
    label = "benign" if prob < 0.5 else "melanoma"

# Persist to SQLite 
    pred = predict_service.save_prediction(
        user_id=current_user.id,
        patient_id=patient_id,
        label=label,
        probability=prob
    )

    return PredictionOut.model_validate(pred)

""" expect a json: {
  "id": 7,
  "user_id": 3,
  "timestamp": "2025-06-17T12:34:56.789Z",
  "label": "benign",
  "probability": 0.42
}
"""

@router.get(
    "/",
    response_model=List[PredictionOut],
    summary="List past predictions for a patient",
)
def read_predictions(
    patient_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_user=Depends(get_current_user),
):
    #enforce that current_user may view this patient:
    patient = patient_service.get_patient(patient_id)
    if not patient:
        raise HTTPException(404, "Patient not found")
    if not current_user.is_admin and patient.owner_id != current_user.id:
        raise HTTPException(403, "Not authorized to view these predictions")

    return predict_service.list_predictions(patient_id, skip=skip, limit=limit)