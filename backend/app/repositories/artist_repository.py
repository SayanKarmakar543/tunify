from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.artist import Artist
from app.repositories.base_repository import BaseRepository


class ArtistRepository(BaseRepository[Artist]):

    def __init__(self, db: AsyncSession):
        super().__init__(db, Artist)
