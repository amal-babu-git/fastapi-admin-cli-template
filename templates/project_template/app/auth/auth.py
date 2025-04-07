from typing import Optional
from fastapi import BackgroundTasks, Request, Depends
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
import logging

from app.auth.models import User
from app.auth.email import send_verification_email
from app.auth.schemas import UserCreate
from app.core.db import get_session
from app.core.settings import settings

logger = logging.getLogger(__name__)

# User Database Dependency
async def get_user_db(session: AsyncSession = Depends(get_session)):
    yield SQLAlchemyUserDatabase(session, User)

# Bearer transport for JWT
bearer_transport = BearerTransport(tokenUrl="api/v1/auth/jwt/login")

# JWT Strategy for authentication
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.JWT_SECRET,
        lifetime_seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

# Authentication backend with JWT
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# User Manager for handling user operations
class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY

    async def create(self, user_create: UserCreate, safe: bool = False, request: Optional[Request] = None) -> User:
        """Override create to control superuser and verification flags."""
        # Force values regardless of what was passed in the request
        user_dict = user_create.model_dump()
        user_dict["is_superuser"] = False
        user_dict["is_verified"] = False
        
        # Create user with the modified dict
        created_user = await super().create(UserCreate(**user_dict), safe, request)
        return created_user
        
    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ) -> None:
        logger.info(f"User {user.id} has registered.")
        
        # Automatically send verification email after registration
        if request:
            try:
                token = self.generate_verification_token(user)
                background_tasks = BackgroundTasks()
                await send_verification_email(user.email, token, background_tasks)
                await background_tasks()
                logger.info(f"Verification email sent for user {user.id}")
            except Exception as e:
                logger.error(f"Failed to send verification email: {str(e)}")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ) -> None:
        logger.info(f"User {user.id} has requested password reset.")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ) -> None:
        if not request:
            logger.warning("Request object is None in on_after_request_verify")
            background_tasks = BackgroundTasks()
            await send_verification_email(user.email, token, background_tasks)
            await background_tasks()
        else:
            background_tasks = getattr(request.state, "background_tasks", BackgroundTasks())
            await send_verification_email(user.email, token, background_tasks)
            logger.info(f"Verification requested for user {user.id}")

# User Manager dependency
async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

# Create FastAPIUsers instance
fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

# Current user dependencies
current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
current_verified_user = fastapi_users.current_user(active=True, verified=True)
