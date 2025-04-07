import uuid
from typing import Optional
from sqlalchemy import Column, String, Boolean
from sqlmodel import Field, SQLModel
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from pydantic import ConfigDict

class User(SQLModel, SQLAlchemyBaseUserTableUUID, table=True):
    """User model that integrates with FastAPI Users and SQLModel."""
    
    __tablename__ = "users"
    
    # Model configuration
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # Base fields required by FastAPI Users
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
    )
    
    email: str = Field(
        index=True,
        nullable=False,
        unique=True,
    )
    
    hashed_password: str = Field(
        nullable=False,
    )
    
    is_active: bool = Field(
        default=True,
        nullable=False,
    )
    
    is_superuser: bool = Field(
        default=False,
        nullable=False,
    )
    
    is_verified: bool = Field(
        default=False,
        nullable=False,
    )
    
    # Custom fields
    first_name: Optional[str] = Field(
        sa_column=Column(String(length=50), nullable=True),
        default=None
    )
    
    last_name: Optional[str] = Field(
        sa_column=Column(String(length=50), nullable=True),
        default=None
    )

    def __repr__(self) -> str:
        return f"<User {self.email}>"
