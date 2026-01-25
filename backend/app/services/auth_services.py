from fastapi import HTTPException, status
from app.db.models.user import User
from app.schemas.user_schema import UserRequest
from app.core.security import hash_password, verify_password
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.security import create_access_token
from datetime import timedelta


async def register_service(db: AsyncSession, user_request: UserRequest) -> User:

    # Check if user already exists
    result = await db.execute(
        select(User).where(User.email == user_request.email)
    )

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Create new user
    new_user = User(
        username = user_request.username,
        email = user_request.email,
        password_hash = hash_password(user_request.password)
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def user_login_service(db: AsyncSession, email: str, password: str) -> User:
    
    # Check authenticate user
    result = await db.execute(
        select(User).where(User.email == email)
    )

    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    
    login_token = create_access_token(
        user.email,
        user.id,
        user.role,
        timedelta(minutes=30)
    )

    return {
        "message": "Login successful!",
        "access_token": login_token,
        "id": str(user.id),
        "role": user.role,
        "token_type": "bearer"
    }


async def get_user_details_service(
    user: dict,
    db: AsyncSession

) -> list[User]:
    
    """
    
    """
    result = await db.execute(select(User).where(User.id == user.id))
    user_details = result.scalar_one_or_none()

    if not user_details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user_details
