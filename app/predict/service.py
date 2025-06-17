
from sqlmodel import Session
from app.database import engine
from app.models import Prediction

def save_prediction(user_id: int, label: str, probability: float) -> Prediction:
    """
    Persist a single prediction record to SQLite and return the saved object
    """
    # new database session 
    with Session(engine) as session:
        # prediction instance 
        pred = Prediction(user_id=user_id, label=label, probability=probability)
        # add to the session/ stage new row 
        session.add(pred)
        # insert into database 
        session.commit()
        # pull back the db generated id and timestamp into pred object 
        session.refresh(pred)
        return pred
