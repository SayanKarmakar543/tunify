from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base import Base
import uuid


class Track(Base):
    __tablename__ = "tracks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False, index=True)
    artist_id = Column(
        UUID(as_uuid=True),
        ForeignKey("artists.id", ondelete="CASCADE"),
        nullable=False
    )
    album_id = Column(
        UUID(as_uuid=True),
        ForeignKey("albums.id", ondelete="SET NULL"),
        nullable=True
    )
    duration = Column(Integer, nullable=False) # in seconds
    file_path = Column(String, nullable=False)
    genre = Column(String, index=True)
    play_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    artist = relationship("Artist", back_populates="tracks")
    album = relationship("Album", back_populates="tracks")
    playlist_tracks = relationship("PlaylistTrack", back_populates="track")
    likes = relationship("Like", back_populates="track")
