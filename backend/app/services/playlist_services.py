from datetime import datetime, timezone
from typing import List, Tuple, Dict
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.playlist import Playlist
from app.repositories.playlist_repository import PlaylistRepository
from app.schemas.playlist_schema import PlaylistCreate, PlaylistUpdate
from app.db.models.user import User
from app.core.exceptions.domain_exception import (
    NotFoundException, 
    ForbiddenException, 
    BadRequestException,
    ValidationException,
    ConflictException
)


class PlaylistService:


    def __init__(
        self,
        *,
        user: User,
        db: AsyncSession,
        playlist_repo: PlaylistRepository
    ):
        self.user = user
        self.db = db
        self.playlist_repo = playlist_repo


    def _current_user_id(self) -> UUID:
        return UUID(self.user.id)


    async def create_playlist(
        self,
        obj_in: PlaylistCreate
    ) -> Playlist:
        payload = {
            "title": obj_in.title,
            "description": obj_in.description,
            "user_id": self._current_user_id()
        }
        return await self.playlist_repo.create(obj_in=payload)


    async def get_playlist_by_id(self, playlist_id: UUID):

        playlist = await self.playlist_repo.get_by_id(playlist_id)
        if not playlist:
            raise NotFoundException("Playlist not found.")
        
        # ownership check
        if playlist.user_id != self._current_user_id():
            raise ForbiddenException("Not allowed to view this playlist")
        
        return playlist


    async def list_my_playlists(
        self,
        *,
        offset: int = 0,
        limit: int = 100
    ) -> Tuple[List[Playlist], int]:
        return await self.playlist_repo.list_by_user(
            user_id=self._current_user_id(),
            offset=offset,
            limit=limit
        )


    async def update_playlist(self, playlist_id: UUID, obj_in: PlaylistUpdate):

        playlist = await self.playlist_repo.get_by_id(playlist_id)

        if not playlist:
            raise NotFoundException("Playlist not found")

        # Locked playlist check
        if playlist.is_locked:
            raise ForbiddenException("Playlist is locked by admin and cannot be modified")

        # Ownership check
        if playlist.user_id != self._current_user_id():
            raise ForbiddenException("Not allowed to update this playlist")

        update_payload = obj_in.model_dump(exclude_unset=True)
        if not update_payload:
            raise BadRequestException("No Fields provided for update.")
        
        # Atleast one meaning change
        no_change = True
        for field, value in update_payload.items():
            if getattr(playlist, field) != value:
                no_change = False
                break

        if no_change:
            raise ValidationException("No change detected")
        
        # Playlist title uniqueness
        if "title" in update_payload and update_payload["title"] != playlist.title:
            title_exist = await self.playlist_repo.exists(
                user_id=self._current_user_id(),
                title=update_payload["title"]
            )
            if title_exist:
                raise ConflictException("Playlist title already exists")
            
        # Title quality rules (not empty, not garbage)
        title = update_payload.get("title")
        if title is not None:
            title = title.strip()
            update_payload["title"] = title

            if not title:
                raise ValidationException("Playlist title cannot be empty")

            if len(title) > 100:
                raise ValidationException("Playlist title is too long")
        
        # Max length limits
        if title is not None and len(title) > 100:
            raise ValidationException("Playlist title is too long")

        return await self.playlist_repo.update(
            db_model=playlist,
            obj_in=update_payload
        )


    async def get_playlist(
        self,
        *,
        playlist_id: UUID
    ) -> Playlist | None:
        playlist = await self.playlist_repo.get_with_tracks(playlist_id)

        if not playlist:
            return None


        return playlist


    async def delete_playlist(self, *, playlist_id: UUID) -> None:
        playlist = await self.playlist_repo.get_by_id(playlist_id)

        if not playlist:
            raise NotFoundException("Playlist not found")
        
        if playlist.is_locked:
            raise ForbiddenException("Playlist is locked by admin")

        if playlist.user_id != self._current_user_id():
            raise ForbiddenException("Not allowed to delete this playlist")

        await self.playlist_repo.delete(db_model=playlist)


    async def lock_playlist(self, playlist_id: UUID, admin: User):
        playlist = await self.playlist_repo.get_by_id(playlist_id)
        if not playlist:
            raise NotFoundException("Playlist not found")

        if playlist.is_locked:
            raise ConflictException("Playlist already locked")

        return await self.playlist_repo.update(
            db_model=playlist,
            obj_in={
                "is_locked": True,
                "locked_by": admin.id,
                "locked_at": datetime.now(timezone.utc),
            }
        )
    

    async def unlock_playlist(self, playlist_id: UUID, admin: User):
        playlist = await self.playlist_repo.get_by_id(playlist_id)

        if not playlist:
            raise NotFoundException("Playlist not found")

        return await self.playlist_repo.update(
            db_model = playlist,
            obj_in={
                "is_locked": False,
                "locked_by": None,
                "locked_at": None,
            }
        )


    async def admin_delete_playlist(self, playlist_id: UUID, admin: User):
        playlist = await self.playlist_repo.get_by_id(playlist_id)

        if not playlist:
            raise NotFoundException("Playlist not found")
        
        await self.playlist_repo.delete(db_model=playlist)
