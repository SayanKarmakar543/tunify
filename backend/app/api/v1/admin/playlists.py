# admin can lock / force-delete playlist.

from fastapi import APIRouter, Depends, status

from uuid import UUID

from app.core.dependencies import admin_only, admin_only
from app.db.models.user import User
from app.services.playlist_services import PlaylistService
from app.core.providers import get_playlist_service
from app.dtos.custom_response_dto import CustomResponseDTO
from app.schemas.playlist_schema import AdminPlaylistResponse

router = APIRouter(
    prefix="/api/v1",
    tags=["Admin-Playlists"]
)

@router.post(
    "/admin/playlists/{playlist_id}/lock",
    status_code=status.HTTP_200_OK,
    response_model=CustomResponseDTO[AdminPlaylistResponse]
)
async def lock_playlist(
    playlist_id: UUID,
    admin: User = Depends(admin_only),
    playlist_service: PlaylistService = Depends(get_playlist_service),
):
    playlist = await playlist_service.lock_playlist(playlist_id, admin)

    return CustomResponseDTO(
        success=True,
        message="Playlist fetched",
        data=playlist,
        total=1,
        status_code=200
    )


@router.post(
    "/admin/playlists/{playlist_id}/unlock",
    status_code=status.HTTP_200_OK,
    response_model=CustomResponseDTO[AdminPlaylistResponse]
)
async def unlock_playlist(
    playlist_id: UUID,
    admin: User = Depends(admin_only),
    playlist_service: PlaylistService = Depends(get_playlist_service),
):
    playlist = await playlist_service.unlock_playlist(playlist_id, admin)

    return CustomResponseDTO(
        success=True,
        message="Playlist unlocked",
        data=playlist,
        total=1,
        status_code=200
    )


@router.delete(
    "/admin/playlists/{playlist_id}",
    status_code=status.HTTP_200_OK,
    response_model=CustomResponseDTO[AdminPlaylistResponse]
)
async def admin_delete_playlist(
    playlist_id: UUID,
    admin: User = Depends(admin_only),
    playlist_service: PlaylistService = Depends(get_playlist_service),
):
    await playlist_service.admin_delete_playlist(playlist_id, admin)

    return CustomResponseDTO(
        success=True,
        message="Playlist deleted successfully",
        data=None,
        total=1,
        status_code=200
    )

