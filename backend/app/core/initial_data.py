# Startup Script to seed an initial admin user into the database

import os
from app.db.models.user import User
from app.core.security import hash_password
from sqlalchemy import select
from app.db.session import async_session_maker
from app.core.config import settings


async def create_initial_admin():
    """
    Creates an admin user on first startup if it does not exist.
    Works with Docker, uvicorn, and FastAPI startup events.
    """

    # admin_email = os.environ.get("TUNIFY_ADMIN_EMAIL")
    # admin_password = os.environ.get("TUNIFY_ADMIN_PASSWORD")

    admin_email = getattr(settings, "TUNIFY_ADMIN_EMAIL", None)
    admin_password = getattr(settings, "TUNIFY_ADMIN_PASSWORD", None)

    print(f"Admin Email: {admin_email}")
    print(f"Admin Password: {admin_password}")

    # If env variables not provided, skip silently
    if not admin_email or not admin_password:
        print("Initial admin env variables not provided. Skipping admin creation.")
        return

    async with async_session_maker() as session:  # this is your correct async session
        result = await session.execute(
            select(User).where(User.email == admin_email)
        )
        existing_user = result.scalars().first()

        if existing_user:
            print(f"Admin {admin_email} already exists. Skipping creation.")
            return

        new_admin = User(
            email=admin_email,
            username=admin_email.split("@")[0],
            password_hash=hash_password(admin_password),
            role="admin",
        )

        session.add(new_admin)
        await session.commit()

        print(f"Created initial admin: {admin_email}")
    