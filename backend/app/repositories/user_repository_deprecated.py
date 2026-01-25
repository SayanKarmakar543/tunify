from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user import User
from sqlalchemy import select
from app.core.dependencies import db_dependency, user_dependency
from uuid import UUID
from typing import TypeVar, Any, Generic, Optional, Dict


ModelType = TypeVar("ModelType", bound=Any)


async def promote_user_to_admin_repo(
    user: user_dependency,
    db: db_dependency,
    user_id: UUID
):
    if user.role != "admin":
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Admin previladges required",
        )

    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User not found",
        )
    user.role = "admin"
    db.add(user)
    await db.commit()
    return user


async def get_all_users_repo(
    user: dict,
    db: AsyncSession

) -> list[User]:
    
    print(f"user: {user}")
    
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    
    result = await db.execute(select(User))

    users = result.scalars().all()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found",
        )

    return users


async def get_users_by_id_repo(
    user: dict,
    db: AsyncSession,
    id: UUID
) -> list[User]:
    
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    
    result = await db.execute(
        select(User).where(User.id == id)
    )

    user_details = result.scalar_one_or_none()

    if not user_details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return user_details
