from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from app.auth.auth import (
    auth_backend, 
    fastapi_users,
    current_active_user,
    current_superuser
)
from app.auth.schemas import UserRead, UserCreate, UserUpdate
from app.auth.models import User

# Create auth router
auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# Add routes for authentication
auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
)

# Add routes for registration
auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/register",
)

# Add routes for reset password
auth_router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/reset-password",
)

# Add routes for verify
auth_router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/verify",
)

# Create users router
users_router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Add routes for user management
users_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
)

# Protected routes example
@auth_router.get("/me")
async def authenticated_route(user: User = Depends(current_active_user)):
    """Example protected route that requires authentication."""
    return {"message": f"Hello {user.email}", "user_id": str(user.id)}

@auth_router.get("/admin")
async def admin_route(user: User = Depends(current_superuser)):
    """Example protected route that requires admin privileges."""
    return {"message": f"Hello admin {user.email}", "user_id": str(user.id)}
