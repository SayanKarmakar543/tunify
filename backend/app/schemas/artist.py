# app/schemas/artist.py

from pydantic import BaseModel, Field, AnyUrl
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from app.dtos.custom_response_dto import CustomResponseDTO


# -------------------------
# Base Schema
# -------------------------
class ArtistBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    bio: Optional[str] = Field(None, max_length=2000)
    profile_image: Optional[AnyUrl] = None


# -------------------------
# Create Schema
# -------------------------
class ArtistCreate(ArtistBase):
    pass


# -------------------------
# Update Schema
# -------------------------
class ArtistUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    bio: Optional[str] = Field(None, max_length=2000)
    profile_image: Optional[AnyUrl] = None


# -------------------------
# Response Schema
# -------------------------
class ArtistResponse(ArtistBase):
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }


# -------------------------
# Response DTO Wrappers
# (IMPORTANT for FastAPI)
# -------------------------
class ArtistResponseDTO(CustomResponseDTO[ArtistResponse]):
    """Single artist response"""
    pass


class ArtistListResponseDTO(CustomResponseDTO[List[ArtistResponse]]):
    """List of artists response"""
    pass
