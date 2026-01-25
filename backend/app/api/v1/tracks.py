from fastapi import APIRouter, Depends, status
from app.core.dependencies import db_dependency, user_dependency
from typing import Annotated
from uuid import UUID


router = APIRouter(
    prefix="/api/v1",
    tags=["Tracks"]
)


@router.get(
    "/tracks",
    status_code=status.HTTP_200_OK,
)
async def get_tracks(
    user: user_dependency,
    db: db_dependency,
):
    pass


@router.get(
    "/tracks/{id}",
    status_code=status.HTTP_200_OK,
)
async def get_track_by_id(
    id: UUID,
    user: user_dependency,
    db: db_dependency,
):
    pass


@router.get(
    "/tracks/{id}/stream",
    status_code=status.HTTP_200_OK,
)
async def stream_track(
    id: UUID,
    user: user_dependency,
    db: db_dependency,
):
    pass


@router.post(
    "/tracks",
    status_code=status.HTTP_201_CREATED,
)
async def create_track(
    user: user_dependency,
    db: db_dependency,
):
    pass


@router.put(
    "/tracks/{id}",
    status_code=status.HTTP_200_OK,
)
async def update_track(
    id: UUID,
    user: user_dependency,
    db: db_dependency,
):
    pass


@router.delete(
    "/tracks/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_track(
    id: UUID,
    user: user_dependency,
    db: db_dependency,
):
    pass


@router.post(
    "/tracks/{id}/increment",
    status_code=status.HTTP_200_OK,
)
async def increment_track_play_count(
    id: UUID,
    user: user_dependency,
    db: db_dependency,
):
    pass
