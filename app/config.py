#centralises secrets and environment settings 

import os
from datetime import timedelta #for jwt token expiry timestamps 

class Settings: 
    #jwt tokens 
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./database.db") #reads environment variable pointing at the database 

settings = Settings() #initiate the Settings class to import a single settings object throughout the app 
