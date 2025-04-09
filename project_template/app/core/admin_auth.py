from typing import Optional
import jwt
from datetime import datetime, timedelta, timezone
import logging
from pydantic import EmailStr

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.settings import settings
from app.auth.auth import get_user_manager, get_user_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_session

# Setup logging
logger = logging.getLogger(__name__)


class AdminAuth(AuthenticationBackend):
    """Authentication backend for the admin interface using JWT."""

    TOKEN_TYPE = "admin"
    ALGORITHM = "HS256"

    async def login(self, request: Request) -> bool:
        """Handle admin login authentication and token creation."""
        try:
            form = await request.form()
            email = form.get("username", "")
            password = form.get("password", "")

            # Basic input validation
            if not email or not password:
                return False

            # Get a user manager instance to validate credentials
            async for session in get_session():
                user_db = await anext(get_user_db(session))
                user_manager = await anext(get_user_manager(user_db))

                try:
                    # Try direct parameter authentication
                    credentials = OAuth2PasswordRequestForm(
                        username=email,
                        password=password,
                        scope=""
                    )
                    user = await user_manager.authenticate(credentials)

                    if not user:
                        return False

                    if not user.is_superuser:
                        logger.warning(
                            f"Non-admin user attempted admin login: {email}")
                        return False

                    # Generate JWT token with appropriate claims
                    token_data = {
                        "sub": str(user.id),
                        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
                        "iat": datetime.now(timezone.utc),
                        "is_superuser": user.is_superuser,
                        "type": self.TOKEN_TYPE,
                        "jti": self._generate_token_id()  # For token revocation
                    }

                    access_token = jwt.encode(
                        token_data,
                        settings.JWT_SECRET,
                        algorithm=self.ALGORITHM
                    )

                    # Set token in session with security parameters
                    request.session.update({"admin_token": access_token})

                    # Set secure cookie parameters if in production
                    if not settings.DEBUG:
                        request.session.setdefault("_session_options", {}).update({
                            "httponly": True,
                            "secure": True,
                            "samesite": "lax"
                        })

                    logger.info(
                        f"Admin user successfully authenticated: {email}")
                    return True

                except jwt.PyJWTError as e:
                    logger.error(f"JWT error during admin login: {str(e)}")
                except Exception as e:
                    logger.error(
                        f"Authentication error for user {email}: {str(e)}")

        except Exception as e:
            logger.error(f"Unexpected error in admin login: {str(e)}")

        return False

    def _generate_token_id(self) -> str:
        """Generate a unique identifier for the token."""
        import uuid
        return str(uuid.uuid4())

    async def logout(self, request: Request) -> bool:
        """Handle admin logout by clearing session."""
        try:
            # Consider adding the token to a blacklist if implementing token revocation
            request.session.clear()
            return True
        except Exception as e:
            logger.error(f"Error during logout: {str(e)}")
            return False

    async def authenticate(self, request: Request) -> bool:
        """Validate the admin token for protected routes."""
        token = request.session.get("admin_token")

        if not token:
            return False

        try:
            # Verify and decode the JWT token
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[self.ALGORITHM],
                options={"verify_signature": True, "verify_exp": True}
            )

            # Check token type
            if payload.get("type") != self.TOKEN_TYPE:
                logger.warning("Invalid token type for admin authentication")
                return False

            # Check if user is a superuser
            if not payload.get("is_superuser", False):
                logger.warning("Non-superuser attempted to access admin area")
                return False

            # Token is valid at this point
            return True

        except jwt.ExpiredSignatureError:
            logger.info("Admin token expired")
            return False
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid admin token: {str(e)}")
            return False
        except Exception as e:
            logger.error(
                f"Unexpected error during admin authentication: {str(e)}")
            return False
