from sqlalchemy import Boolean, Column, String, ForeignKey, Text, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid


class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Admin moderation fields
    is_locked = Column(Boolean, default=False, nullable=False)
    locked_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    locked_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="playlists"
    )

    locked_by_user = relationship(
        "User",
        foreign_keys=[locked_by],
        lazy="joined"
    )

    playlist_tracks = relationship(
        "PlaylistTrack",
        back_populates="playlist",
        cascade="all, delete-orphan"
    )

