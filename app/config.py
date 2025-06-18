#centralises secrets and environment settings 

import os
from datetime import timedelta #for jwt token expiry timestamps 

class Settings: 
    #jwt tokens 
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    EMAIL_VERIFY_EXPIRE_MINUTES: int = 15   # tokens to verify e-mail live for 15 mins
    
    # Where your front-end will consume the verification link
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

    # Database connection
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./database.db")

settings = Settings() #initiate the Settings class to import a single settings object throughout the app 
