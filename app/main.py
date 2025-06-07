#wires everything into a live FastAPI server; mounts routers and runs the database 

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_db
from app.auth.router import router as auth_router
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # **Startup**: create your SQLite tables
    init_db()
    yield      # <-- the application runs here; hand-off point between setup and teardown in the context-manager pattern
    # **Shutdown**: place any teardown logic here if needed

app = FastAPI(
    title="Melanoma Detection API",
    description="Upload dermoscopic images and receive melanoma probability scores",
    version="0.1.0",
    lifespan=lifespan
)

# include authentication endpoints
app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.get("/", tags=["root"])
def read_root():
    return {"message": "Welcome to the Melanoma Detection API"}
