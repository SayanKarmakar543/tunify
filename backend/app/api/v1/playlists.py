from fastapi import APIRouter, Depends, status
from app.core.dependencies import db_dependency, user_dependency
from typing import Annotated
from uuid import UUID


router = APIRouter(
    prefix="/api/v1",
    tags=["Playlists"]
)


@router.get(
    "/playlists",
    status_code=status.HTTP_200_OK,
)
async def get_playlists(
    user: user_dependency,
    db: db_dependency,
):
    pass


@router.get(
    "/users/{user_id}/playlists",
    status_code=status.HTTP_200_OK,
)
async def get_user_playlists(
    user_id: UUID,
    user: user_dependency,
    db: db_dependency,
):
    pass


@router.post(
    "/playlists",
    status_code=status.HTTP_201_CREATED,
)
async def create_playlist(
    user: user_dependency,
    db: db_dependency,
):
    pass


@router.get(
    "/playlists/{id}",
    status_code=status.HTTP_200_OK,
)
async def get_playlist_by_id(
    id: UUID,
    user: user_dependency,
    db: db_dependency,
):
    pass


@router.put(
    "/playlists/{id}",
    status_code=status.HTTP_200_OK,
)
async def update_playlist(
    id: UUID,
    user: user_dependency,
    db: db_dependency,
):
    pass


@router.delete(
    "/playlists/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_playlist(
    id: UUID,
    user: user_dependency,
    db: db_dependency,
):
    pass


@router.post(
    "/playlists/{id}/tracks",
    status_code=status.HTTP_201_CREATED,
)
async def add_track_to_playlist(
    id: UUID,
    user: user_dependency,
    db: db_dependency,
):
    pass


@router.delete(
    "/playlists/{id}/tracks/{track_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_track_from_playlist(
    id: UUID,
    track_id: UUID,
    user: user_dependency,
    db: db_dependency,
):
    pass


@router.patch(
    "/playlists/{id}/reorder",
    status_code=status.HTTP_200_OK,
)
async def reorder_playlist_tracks(
    id: UUID,
    user: user_dependency,
    db: db_dependency,
):
    pass
