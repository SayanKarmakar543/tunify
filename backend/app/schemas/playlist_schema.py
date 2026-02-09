from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID


class PlaylistBase(BaseModel):
    title: str
    description: str | None = None


class PlaylistCreate(PlaylistBase):
    pass


class PlaylistUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class PlaylistResponse(PlaylistBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
    }


class AdminPlaylistResponse(PlaylistResponse):
    is_locked: bool
    locked_by: Optional[UUID]
    locked_at: Optional[datetime]

    model_config = {
        "from_attributes": True,
    }
