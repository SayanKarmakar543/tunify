from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):

    def __init__(self, db: AsyncSession):
        super().__init__(db, User)
