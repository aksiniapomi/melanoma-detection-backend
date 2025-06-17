# eveyr /predict response returns a float probability and label string 
# schemas.py inside each feature-area folder 
# request/response models 

from datetime import datetime
from sqlmodel import SQLModel

class PredictionOut(SQLModel):
    id: int
    user_id: int
    timestamp: datetime
    label: str
    probability: float

    class Config:
        orm_mode = True

#tells FastAPI POST /predict return JSON object 
# { "probability": 0.42, "label": "benign" }
