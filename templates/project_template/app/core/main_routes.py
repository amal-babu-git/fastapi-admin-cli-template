"""
This module consolidates all API routes into a single router.
"""

from fastapi import APIRouter

# Main router that will include all other routers
main_router = APIRouter()

# API version
api_version = "v1"

# Import and include the authentication router
from app.auth.routes import auth_router, users_router
main_router.include_router(
    auth_router,
    prefix=f"/api/{api_version}",
    tags=["auth"]
)
main_router.include_router(
    users_router,
    prefix=f"/api/{api_version}",
    tags=["users"]
)

# Import and include your app-specific routers here
# Example:
# from app.your_module.routes import your_router
# main_router.include_router(
#     your_router,
#     prefix=f"/api/{api_version}/your-endpoint",
#     tags=["your-tag"]
# )
