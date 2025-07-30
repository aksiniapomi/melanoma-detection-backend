#centralises secrets and environment settings 

import os
from datetime import timedelta #for jwt token expiry timestamps 
from dotenv import load_dotenv

load_dotenv() #reads .env into os.environ 

class Settings: 
    #jwt tokens 
    SECRET_KEY: str = os.getenv("SECRET_KEY", "fallback-secret")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    EMAIL_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("EMAIL_TOKEN_EXPIRE_MINUTES", "15"))   # tokens to verify e-mail live for 15 mins
    
    # Where your front-end will consume the verification link
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

    # Database connection
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./database.db")

    SENDGRID_API_KEY: str = os.getenv("SENDGRID_API_KEY", "")
    EMAIL_FROM_ADDRESS: str   = os.getenv("EMAIL_FROM_ADDRESS", "noreply@example.com")

settings = Settings() #initiate the Settings class to import a single settings object throughout the app 
