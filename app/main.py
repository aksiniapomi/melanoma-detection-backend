#wires everything into a live FastAPI server; mounts routers and runs the database 

from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
from app.database import init_db
from app.auth.router import router as auth_router
from app.auth.admin_router import router as admin_router
from app.predict.router import router as predict_router
from app.patient.router import router as patient_router
from app.middleware.rate_limiter import RateLimiterMiddleware
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create SQLite tables
    init_db()
    yield      #the application runs here; hand-off point between setup and teardown in the context-manager pattern
    # Shutdown: any teardown logic here

# per-path limits 
rate_limit_rules = {
    "/auth/login":    (5,   60),    # max 5 login attempts per minute
    "/auth/refresh":  (10,  60),    # max 10 refreshes per minute
    "/predict":       (20, 3600),   # max 20 predictions per hour
}

app = FastAPI(
    title="Melanoma Detection API",
    description="Upload dermoscopic images and receive melanoma probability scores",
    version="0.1.0",
    lifespan=lifespan
)

debug_router = APIRouter()

@debug_router.get("/_debug/env")
def dump_env():
    return {
        "SMTP_HOST":  os.getenv("SMTP_HOST"),
        "SMTP_PORT":  os.getenv("SMTP_PORT"),
        "SMTP_USER":  os.getenv("SMTP_USER"),
        "SMTP_PASS":  bool(os.getenv("SMTP_PASS")),
        "EMAIL_FROM": os.getenv("EMAIL_FROM_ADDRESS"),
    }

app.include_router(debug_router, tags=["debug"])

#rate-limiter middleware
app.add_middleware(RateLimiterMiddleware, rules=rate_limit_rules)

# Mount patient routes at /patients
app.include_router(patient_router, prefix="/patients", tags=["patients"])

# include authentication endpoints
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# include predict endpoint 
app.include_router(predict_router, prefix="/predict", tags=["predictions"])

app.include_router(admin_router, prefix="/admin", tags=["admin"])

@app.get("/", tags=["root"])
def read_root():
    return {"message": "Welcome to the Melanoma Detection API"}
