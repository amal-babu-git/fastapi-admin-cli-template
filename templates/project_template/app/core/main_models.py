"""
This module consolidates all SQLModel models to make them available for Alembic migrations.
Import all your models here so that they're included in migrations.
"""

from sqlmodel import SQLModel

# Import all your models here
from app.auth.models import User

# Import your app-specific models here
# Example:
# from app.your_module.models import YourModel
