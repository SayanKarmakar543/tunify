from fastapi import APIRouter, Depends, status, Query
from app.core.dependencies import db_dependency, user_dependency
from typing import List
from uuid import UUID
from app.dtos.custom_response_dto import CustomResponseDTO
from app.schemas.playlist_schema import PlaylistResponse, PlaylistCreate, PlaylistUpdate
from app.core.providers import get_playlist_service
from app.services.playlist_services import PlaylistService


router = APIRouter(
    prefix="/api/v1",
    tags=["Playlists"]
)


@router.get(
    "/playlists",
    status_code=status.HTTP_200_OK,
    response_model=CustomResponseDTO[List[PlaylistResponse]]
)
async def get_playlists(
    playlist_service: PlaylistService = Depends(get_playlist_service),
    offset: int = Query(0, ge=0),
    limit: int = Query(25, ge=1, le=100),
):
    playlist, total = await playlist_service.list_my_playlists(offset=offset, limit=limit)
    return CustomResponseDTO(
        success=True,
        message="Playlist fatched.",
        data=playlist,
        total=total,
        status_code=200
    )


@router.get(
    "/users/{user_id}/playlists",
    status_code=status.HTTP_200_OK,
    response_model=CustomResponseDTO[List[PlaylistResponse]]
)
async def get_user_playlists(
    playlist_service: PlaylistService = Depends(get_playlist_service),
    offset: int = Query(0, ge=0),
    limit: int = Query(25, ge=1, le=100),
):
    pass


@router.post(
    "/playlists",
    status_code=status.HTTP_201_CREATED,
    response_model=CustomResponseDTO[PlaylistResponse]
)
async def create_playlist(
    playlist_request: PlaylistCreate,
    playlist_service: PlaylistService = Depends(get_playlist_service)
):
    playlist = await playlist_service.create_playlist(
        obj_in=playlist_request
    )
    return CustomResponseDTO(
        success=True,
        message="Playlist created successfully",
        data=playlist,
        total=1,
        status_code=201
    )


@router.get(
    "/playlists/{playlist_id}",
    status_code=status.HTTP_200_OK,
    response_model=CustomResponseDTO[PlaylistResponse]
)
async def get_playlist_by_id(
    playlist_id: UUID,
    playlist_service: PlaylistService = Depends(get_playlist_service),
):
    playlist = await playlist_service.get_playlist_by_id(playlist_id=playlist_id)

    return CustomResponseDTO(
        success=True,
        message="Playlist fetched",
        data=playlist,
        total=1,
        status_code=200
    )


@router.put(
    "/playlists/{playlist_id}",
    status_code=status.HTTP_200_OK,
    response_model=CustomResponseDTO[PlaylistResponse]
)
async def update_playlist(
    playlist_id: UUID,
    playlist_request: PlaylistUpdate,
    playlist_service: PlaylistService = Depends(get_playlist_service)
):
    
    playlist = await playlist_service.update_playlist(
        playlist_id=playlist_id, 
        obj_in=playlist_request
    )

    return CustomResponseDTO(
        success=True,
        message="Playlist updated",
        data=playlist,
        total=1,
        status_code=200
    )


@router.delete(
    "/playlists/{playlist_id}",
    response_model=CustomResponseDTO[None],
    status_code=status.HTTP_200_OK
)
async def delete_playlist(
    playlist_id: UUID,
    playlist_service: PlaylistService = Depends(get_playlist_service)
):
    await playlist_service.delete_playlist(playlist_id=playlist_id)

    return CustomResponseDTO(
        success=True,
        message="Playlist deleted successfully",
        data=None,
        total=1,
        status_code=200
    )


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
