from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.db.models import (
    user,
    playlist,
    like,
    refresh_token,
    album,
    artist,
    track,
    playlist_track
)
