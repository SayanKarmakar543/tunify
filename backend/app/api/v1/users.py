from fastapi import APIRouter, Depends, status, Query
from uuid import UUID
from typing import Optional, List

from app.services.user_services import UserService
from app.core.providers import get_user_service
from app.dtos.custom_response_dto import CustomResponseDTO
from app.db.models.user import User
from app.core.dependencies import admin_only
from app.schemas.user_schema import(
    UserResponse, 
    UserCreate,
    UserUpdateRequest
)


router = APIRouter(
    prefix="/api/v1",
    tags=["Users"]
)


@router.get(
    "/users",
    response_model=CustomResponseDTO[List[UserResponse]],
    status_code=status.HTTP_200_OK,
)
async def get_all_users(
    user_service: UserService = Depends(get_user_service),
    offset: int = Query(0, ge=0),
    limit: int = Query(25, ge=1, le=100),
    name: Optional[str] = Query(None),
    _: User = Depends(admin_only)
):
    filters = {}
    if name:
        filters["name"] = name

    users, total = await user_service.get_users(
        offset=offset,
        limit=limit,
        filters=filters,
    )

    return CustomResponseDTO(
        success=True,
        message="Users fetched",
        data=users,
        total=total,
        status_code=200,
    )


@router.get(
    "/users/{id}",
    response_model=CustomResponseDTO[UserResponse],
    status_code=status.HTTP_200_OK,
)
async def get_user_by_id(
    id: UUID,
    user_service: UserService = Depends(get_user_service),
    _: User = Depends(admin_only)
):
    user = await user_service.get_user_by_id(user_id=id)

    return CustomResponseDTO(
        success=True,
        message="User fetched",
        data=user,
        total=1,
        status_code=200,
    )


@router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    response_model=CustomResponseDTO[UserResponse],
)
async def create_user(
    user_request: UserCreate,
    user_service: UserService = Depends(get_user_service),
    _: User = Depends(admin_only)
):
    user = await user_service.create_user(obj_in=user_request)

    return CustomResponseDTO(
        success=True,
        message="User created",
        data=user,
        total=1,
        status_code=201,
    )


@router.put(
    "/users/{id}",
    status_code=status.HTTP_200_OK,
    response_model=CustomResponseDTO[UserResponse],
)
async def update_user(
    id: UUID,
    user_request: UserUpdateRequest,
    user_service: UserService = Depends(get_user_service),
    _: User = Depends(admin_only)
):
    user = await user_service.update_user(
        user_id=id,
        obj_in=user_request
    )

    return CustomResponseDTO(
        success=True,
        message="User updated",
        data=user,
        total=1,
        status_code=200,
    )


@router.delete(
    "/users/{id}",
    response_model=CustomResponseDTO[None],
    status_code=status.HTTP_200_OK,
)
async def delete_user(
    id: UUID,
    user_service: UserService = Depends(get_user_service),
    _: User = Depends(admin_only)
):
    await user_service.delete_user(id)

    return CustomResponseDTO(
        success=True,
        message="User deleted successfully",
        data=None,
        total=1,
        status_code=200,
    )
