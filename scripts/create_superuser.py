#!/usr/bin/env python
from fastapi_users.password import PasswordHelper
from app.core.db import async_session_factory
from sqlalchemy import text
import asyncio
import sys
import uuid
import argparse
from pathlib import Path

# Add the project root to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

"""
IMPORTANT: Since the database is dockerized, run this script using:

docker-compose -f docker/compose/docker-compose.yml run --rm api python scripts/create_superuser.py <email> <password> [--first-name FIRST_NAME] [--last-name LAST_NAME]

Example:
docker-compose -f docker/compose/docker-compose.yml run --rm api python scripts/create_superuser.py admin@example.com mypassword --first-name Admin --last-name User
"""


async def create_superuser(email, password, first_name=None, last_name=None):
    """Create a superuser account for admin panel access."""
    try:
        # Create password helper for hashing
        password_helper = PasswordHelper()
        hashed_password = password_helper.hash(password)

        # Generate a UUID for the new user
        user_id = str(uuid.uuid4())

        async with async_session_factory() as session:
            # Check if user already exists
            result = await session.execute(
                text("SELECT id, is_superuser FROM users WHERE email = :email"),
                {"email": email}
            )
            user = result.fetchone()

            if user:
                print(f"User with email {email} already exists.")

                # Update to superuser if needed
                if not user.is_superuser:
                    await session.execute(
                        text(
                            "UPDATE users SET is_superuser = TRUE, is_verified = TRUE WHERE email = :email"),
                        {"email": email}
                    )
                    await session.commit()
                    print(f"Updated user {email} to superuser status.")
                return

            # Create new superuser
            await session.execute(
                text("""
                INSERT INTO users (
                    id, email, hashed_password, is_active, 
                    is_superuser, is_verified, first_name, last_name
                ) VALUES (
                    :id, :email, :hashed_password, TRUE,
                    TRUE, TRUE, :first_name, :last_name
                )
                """),
                {
                    "id": user_id,
                    "email": email,
                    "hashed_password": hashed_password,
                    "first_name": first_name,
                    "last_name": last_name
                }
            )

            await session.commit()
            print(f"✓ Superuser {email} created successfully!")

    except Exception as e:
        print(f"Error creating superuser: {str(e)}")
        raise


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Create a superuser for the admin panel")
    parser.add_argument("email", help="Email address for the superuser")
    parser.add_argument("password", help="Password for the superuser")
    parser.add_argument("--first-name", help="First name of the superuser")
    parser.add_argument("--last-name", help="Last name of the superuser")

    args = parser.parse_args()

    # Run the async function
    asyncio.run(create_superuser(
        args.email,
        args.password,
        args.first_name,
        args.last_name
    ))
