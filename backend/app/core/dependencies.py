# app/core/dependencies.py
"""
Dependency injection utilities for Tunify.

- oauth2_bearer: used by FastAPI/OpenAPI to show "Authorize" (bearer) in Swagger UI.
- get_current_user: validates JWT, returns User SQLAlchemy model instance.
- admin_required: ensures user has admin role.
- user_dependency / db_dependency: typed Annotated dependencies for endpoints.
"""

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.core.config import settings
from app.db.session import get_db
from app.db.models.user import User, UserRole


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_bearer), 
    db: AsyncSession = Depends(get_db)
) -> User:
    
    """
    Validate the incoming JWT access token and return the corresponding User instance.

    Expectations:
      - Token contains `sub` claim as user id (int or string of int).
      - Token is signed with `settings.SECRET_KEY` and algorithm `settings.ALGORITHM`.
      - Raises 401 for invalid/expired token, 404 if user not found.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        user_email: str = payload.get("sub")
        user_id: uuid = payload.get("id")
        role: str = payload.get("role")

        if user_email is None or user_id is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return User(
            id=user_id,
            email=user_email,
            role=role
        )
    
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


async def admin_required(current_user: User):
    """
    Ensure the current user has admin privileges.
    Adjust the role check according to your User model (role name / enum).
    """

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )


def admin_only(user: User = Depends(get_current_user)):
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return user

user_dependency = Annotated[User, Depends(get_current_user)]
db_dependency = Annotated[AsyncSession, Depends(get_db)]
