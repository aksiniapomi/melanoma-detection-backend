
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine
from sqlmodel import SQLModel

@pytest.fixture(scope="module")
def client():
    # ensure all tables exist
    SQLModel.metadata.create_all(engine, checkfirst=True)

    with TestClient(app) as c:
        yield c
