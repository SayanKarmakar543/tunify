# app/services/artist_service.py
from typing import List, Optional, Dict, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.artist_repository import ArtistRepository
from app.db.models.artist import Artist
# from app.services.user_services import UserService

class ArtistService:
    def __init__(
        self,
        *,
        user: dict,   # Dependency injected UserService / Composition
        db: AsyncSession,
        artist_repo: ArtistRepository
    ):
        self.user = user
        self.db = db
        self.artist_repo = artist_repo

    # async def get_artists(self, offset, limit, filters: Optional[Dict] = None) -> List[Artist]:
    #     items = await self.artist_repo.list(offset=offset, limit=limit, filters=filters)
    #     return items


    # def get_user(self) -> Optional[Dict]:
    #     return self.user.get_user()
    

    async def list_artists(self, *, offset: int = 0, limit: int = 100, filters: Optional[Dict] = None) -> Tuple[List[Artist], int]:
        items, total = await self.artist_repo.list(offset=offset, limit=limit, filters=filters)
        return items, total


    # async def create_artist(self, payload: Dict):
    #     # payload is validated Pydantic dict
    #     return await self.artist_repo.create(obj_in=payload)

    # async def update_artist(self, id, payload: Dict):
    #     return await self.artist_repo.update(id=id, obj_in=payload)

    # async def delete_artist(self, id):
        # return await self.artist_repo.delete(id=id)
