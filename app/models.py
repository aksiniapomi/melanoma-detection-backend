
from sqlmodel import SQLModel

import app.patient.models    # registers Patient
import app.predict.models    # registers Prediction with FKs
import app.auth.models       # registers User, etc.

