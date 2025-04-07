"""
Database models for the ${app_name} app.
"""
from typing import Optional
from datetime import datetime
import uuid
from sqlmodel import Column, Field, SQLModel
import sqlalchemy.dialects.postgresql as pg


class ${model_name}(SQLModel, table=True):
    """${model_description}"""
    __tablename__ = "${table_name}"

    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    # Add your model fields here
    # Example:
    # title: str = Field(index=True)
    # content: Optional[str] = Field(default=None)
    
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    
    def __repr__(self):
        return f"<${model_name}(id={self.id})>"
