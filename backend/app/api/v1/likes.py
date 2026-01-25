from fastapi import APIRouter, Depends, status
from app.core.dependencies import db_dependency, user_dependency
from typing import Annotated
from uuid import UUID


router = APIRouter(
    prefix="/api/v1",
    tags=["Likes"]
)


@router.post(
    "/tracks/{track_id}/like",
    status_code=status.HTTP_201_CREATED,
)
async def like_track(
    track_id: UUID,
    user: user_dependency,
    db: db_dependency,
):
    pass


@router.get(
    "/users/{user_id}/likes",
    status_code=status.HTTP_200_OK,
)
async def get_user_likes(
    user_id: UUID,
    user: user_dependency,
    db: db_dependency,
):
    pass
