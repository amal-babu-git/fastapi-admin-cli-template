"""
Pydantic schemas for the ${app_name} app.
"""
from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, Field


class ${model_name}Base(BaseModel):
    """Base schema for ${app_name}."""
    # Add your base fields here
    # Example:
    # title: str = Field(..., example="Example title")
    # content: Optional[str] = Field(None, example="Example content")
    pass


class ${model_name}Create(${model_name}Base):
    """Schema for creating a new ${app_name}."""
    pass


class ${model_name}Update(BaseModel):
    """Schema for updating an existing ${app_name}."""
    # Add your update fields here
    # Example:
    # title: Optional[str] = Field(None, example="Updated title")
    # content: Optional[str] = Field(None, example="Updated content")
    pass


class ${model_name}Read(${model_name}Base):
    """Schema for reading ${app_name} data."""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
