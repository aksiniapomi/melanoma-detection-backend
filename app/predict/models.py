
from sqlmodel import SQLModel, Field
from uuid import uuid4

class Prediction(SQLModel, table=True):
    id: int = Field(default_factory=lambda: uuid4().int, primary_key=True)

