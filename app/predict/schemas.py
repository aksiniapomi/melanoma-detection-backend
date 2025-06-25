# eveyr /predict response returns a float probability and label string 
# schemas.py inside each feature-area folder 
# request/response models 

from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class PredictionOut(BaseModel):
    id: UUID
    user_id: int
    patient_id: int
    timestamp: datetime
    label: str
    probability: float

    class Config:
        from_attributes = True

#tells FastAPI POST /predict return JSON object 
# { "probability": 0.42, "label": "benign" }
