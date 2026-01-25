# app/services/user_services.py

# app/services/user_services.py

from uuid import UUID
from typing import Dict, List, Tuple

from pydantic import field_validator
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import admin_required
from app.db.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserUpdateRequest
from app.core.security import hash_password
from app.domain.validators.password_validator import validate_password
from app.core.exceptions.domain_exception import (
    ConflictException,
    NotFoundException,
    ValidationException
)


class UserService:


    def __init__(
        self,
        *,
        user: Dict,
        db: AsyncSession,
        user_repo: UserRepository
    ):
        self.user = user
        self.db = db
        self.user_repo = user_repo

   
    async def get_users(
        self,
        offset: int,
        limit: int,
        filters: dict,
    ) -> Tuple[List[User], int]:

        users, total = await self.user_repo.list(
            offset=offset,
            limit=limit,
            filters=filters,
        )

        # Empty list is valid → no exception needed
        return users, total


    async def get_user_by_id(self, user_id: UUID) -> User:

        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")

        return user

  
    async def create_user(self, obj_in: UserCreate) -> User:

        if await self.user_repo.exists(email=obj_in.email):
            raise ConflictException("Email already registered")

        if await self.user_repo.exists(username=obj_in.username):
            raise ConflictException("Username already taken")
        
        validate_password(obj_in.password)

        hashed_password = hash_password(obj_in.password)

        db_obj = obj_in.model_dump(
            exclude={"password"},
            exclude_none=True,
        )
        db_obj["password_hash"] = hashed_password

        return await self.user_repo.create(obj_in=db_obj)


    async def update_user(
        self,
        user_id: UUID,
        obj_in: UserUpdateRequest
    ) -> User:
        user = await self.user_repo.get_by_id(user_id)

        if not user:
            raise NotFoundException("User not found.")
        
        update_data = obj_in.model_dump(exclude_unset=True)

        if not update_data:
            raise ValidationException("No data provided for update.")

        if "email" in update_data and update_data["email"] != user.email:
            if await self.user_repo.exists(email=update_data["email"]):
                raise ConflictException("Email already registered")

        if "username" in update_data and update_data["username"] != user.username:
            if await self.user_repo.exists(username=update_data["username"]):
                raise ConflictException("Username already taken")
        
        return await self.user_repo.update(db_model=user, obj_in=update_data)


    async def delete_user(self, user_id: UUID) -> None:
        user = await self.user_repo.get_by_id(user_id)

        if not user:
            raise NotFoundException("User not found.")

        await self.user_repo.delete(db_model=user)

