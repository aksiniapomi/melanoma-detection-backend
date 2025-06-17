# eveyr /predict response returns a float probability and label string 
# schemas.py inside each feature-area folder 
# request/response models 

from pydantic import BaseModel

class PredictionOut(BaseModel):
    probability: float
    label:       str

#tells FastAPI POST /predict return JSON object 
# { "probability": 0.42, "label": "benign" }
