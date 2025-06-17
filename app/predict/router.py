
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.auth.dependencies import get_current_user
from app.predict.schemas import PredictionOut

router = APIRouter()

@router.post("", response_model=PredictionOut)
async def predict(
    image: UploadFile = File(...),
    user=Depends(get_current_user) #only logged-in users can call /predict 
):
    """
    Stub /predict endpoint.
    Accepts an image upload and returns a dummy melanoma probability.
    """
    # verify file type
    if image.content_type.split("/")[0] != "image":
        raise HTTPException(400, "Please upload an image file")
    # read bytes (we won't do anything with them yet)
    data = await image.read()

    # TODO: replace this with real ML inference
    dummy_prob = 0.42
    dummy_label = "benign" if dummy_prob < 0.5 else "melanoma"

    return PredictionOut(probability=dummy_prob, label=dummy_label)
