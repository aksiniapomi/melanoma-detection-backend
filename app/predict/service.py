
from sqlmodel import Session, select 
from app.database import engine
from app.predict.models import Prediction
from sqlalchemy.exc import IntegrityError
import logging
from typing import List 

logger = logging.getLogger("uvicorn.error")

def save_prediction(
    user_id: int,
    patient_id: int,                  
    label: str,
    probability: float
) -> Prediction:
    
    """
    Persist a single prediction record to SQLite and return the saved object
    """
    # new database session 
    with Session(engine) as session:
        # prediction instance 
        pred = Prediction(
            user_id=user_id,
            patient_id=patient_id,      #store FK
            label=label,
            probability=probability
        )
        # add to the session/ stage new row 
        session.add(pred)
        
        try:
            session.commit()
        except IntegrityError as e:
            session.rollback()
            # this is the real DB complaint
            logger.error("DB IntegrityError: %s", e.orig)
            # re-raise so that Uvicorn still returns 500
            raise
        
        # insert into database 
        #session.commit()
        # pull back the db generated id and timestamp into pred object 
        session.refresh(pred)
        return pred

def list_predictions(
    patient_id: int,
    skip: int = 0,
    limit: int = 100,
) -> List[Prediction]:
    with Session(engine) as session:
        stmt = (
            select(Prediction)
            .where(Prediction.patient_id == patient_id)
            .offset(skip)
            .limit(limit)
        )
        return session.exec(stmt).all()