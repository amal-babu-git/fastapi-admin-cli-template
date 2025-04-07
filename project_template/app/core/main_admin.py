"""
This module provides functionality to set up an admin interface for a FastAPI application using SQLAdmin.
It includes a decorator for registering admin views and a function to initialize the admin interface.
"""

from sqladmin import Admin
from app.core.db import engine
from fastapi import FastAPI
from typing import List, Type
from sqladmin.models import ModelView
import importlib
import logging

logger = logging.getLogger(__name__)

# Global registry to store admin classes
admin_views: List[Type[ModelView]] = []

def register_admin(cls: Type[ModelView]) -> Type[ModelView]:
    """
    Register an admin view class to the global registry.
    
    Args:
        cls (Type[ModelView]): The admin view class to register.
        
    Returns:
        Type[ModelView]: The same class that was registered.
    """
    admin_views.append(cls)
    return cls

def setup_admin(app: FastAPI) -> None:
    """
    Initialize the admin interface for the FastAPI application.
    
    Args:
        app (FastAPI): The FastAPI application instance.
    """
    admin = Admin(app, engine)
    
    # Import admin modules - update these imports based on your app structure
    try:
        # These will be dynamically imported based on your project structure
        # Default authentication admin
        import app.auth.admin
        
        # Your application modules should be imported here
        # Example:
        # import app.your_module.admin
        
        # Register all views to admin
        for view in admin_views:
            admin.add_view(view)
            logger.info(f"Registered admin view: {view.__name__}")
            
    except ImportError as e:
        logger.warning(f"Error importing admin module: {e}")
