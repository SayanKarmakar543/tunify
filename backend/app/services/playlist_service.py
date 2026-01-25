from typing import List, Tuple
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.playlist import Playlist
from app.repositories.playlist_repository import PlaylistRepository


class PlaylistService:

    def __init__(
        self,
        *,
        user: dict,                 # injected from dependency
        db: AsyncSession,
        playlist_repo: PlaylistRepository
    ):
        self.user = user
        self.db = db
        self.playlist_repo = playlist_repo

    def _current_user_id(self) -> UUID:
        return self.user["id"]

    async def create_playlist(
        self,
        *,
        title: str,
        description: str | None = None
    ) -> Playlist:
        payload = {
            "title": title,
            "description": description,
            "user_id": self._current_user_id()
        }
        return await self.playlist_repo.create(obj_in=payload)

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

    async def get_playlist(
        self,
        *,
        playlist_id: UUID
    ) -> Playlist | None:
        playlist = await self.playlist_repo.get_with_tracks(playlist_id)

        if not playlist:
            return None

        # ownership check
        if playlist.user_id != self._current_user_id():
            return None

        return playlist

    async def delete_playlist(self, *, playlist_id: UUID) -> bool:
        playlist = await self.playlist_repo.read(playlist_id)

        if not playlist:
            return False

        if playlist.user_id != self._current_user_id():
            return False

        await self.playlist_repo.delete(id=playlist_id)
        return True
