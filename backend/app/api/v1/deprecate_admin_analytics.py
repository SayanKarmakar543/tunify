from fastapi import APIRouter, Depends, status

from uuid import UUID

from app.core.dependencies import db_dependency, user_dependency
from app.repositories.user_repository_deprecated import (
    promote_user_to_admin_repo,
)

router = APIRouter(
    prefix="/api/v1",
    tags=["Admin-Analytics"]
)


@router.get(
    "/admin/analytics/top-tracks",
    status_code=status.HTTP_200_OK,
)
async def get_top_tracks(
    user: user_dependency,
    db: db_dependency,
):
    pass


@router.get(
    "/admin/analytics/actice-users",
    status_code=status.HTTP_200_OK,
)
async def get_active_users(
    user: user_dependency,
    db: db_dependency,
):
    pass


@router.post(
    "/admin/users/{user_id}/promote",
    status_code=status.HTTP_200_OK,
)
async def promote_user_to_admin(
    user: user_dependency,
    db: db_dependency,
    user_id: UUID
):
    return await promote_user_to_admin_repo(
        user, db, user_id
    )
