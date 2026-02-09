from typing import List, Tuple
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.playlist import Playlist
from app.repositories.base_repository import BaseRepository 


class PlaylistRepository(BaseRepository[Playlist]):


    def __init__(self, db: AsyncSession):
        super().__init__(db, Playlist)


    async def list_by_user(
        self,
        *,
        user_id: UUID,
        offset: int = 0,
        limit: int = 100
    ) -> Tuple[List[Playlist], int]:
        """
        Get playlists created by a specific user
        """
        return await self.list(
            offset=offset,
            limit=limit,
            filters={"user_id": user_id}
        )


    async def get_with_tracks(self, playlist_id: UUID) -> Playlist | None:
        """
        Fetch playlist along with tracks
        """
        query = (
            select(Playlist)
            .where(Playlist.id == playlist_id)
            .options(
                selectinload(Playlist.playlist_tracks)
                .selectinload("track")
            )
        )

        result = await self.db.execute(query)
        return result.scalars().first()
