
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.auth.dependencies import get_current_user
from app.predict.schemas import PredictionOut
from app.predict import service as predict_service
from pathlib import Path 

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