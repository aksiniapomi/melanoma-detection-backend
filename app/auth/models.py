#how users are stored in the database; the Users table in the database 

from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str     = Field(index=True, unique=True)
    email: str        = Field(unique=True, index=True)
    hashed_password: str
    is_verified: bool = Field(default=False, description="Has the user confirmed their e-mail?")
    created_at: datetime = Field(
           default_factory=lambda: datetime.now(timezone.utc),
           description="UTC timestamp when the user was created"
   )

class BlacklistedToken(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    jti: str          = Field(..., description="JWT ID to revoke")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp When this token was blacklisted"
    ) 
    
    