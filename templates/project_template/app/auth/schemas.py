from typing import Optional
from pydantic import EmailStr
import uuid
from fastapi_users import schemas

class UserRead(schemas.BaseUser):
    """Schema for user data returned from the API."""
    id: uuid.UUID
    email: EmailStr
    is_active: bool
    is_superuser: bool
    is_verified: bool
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    
    class Config:
        orm_mode = True

class UserCreate(schemas.BaseUserCreate):
    """Schema for creating a new user."""
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "strong-password",
                "first_name": "John",
                "last_name": "Doe"
            }
        }

    # These fields will be forced to these values
    is_superuser: bool = False
    is_verified: bool = False

class UserUpdate(schemas.BaseUserUpdate):
    """Schema for updating an existing user."""
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
