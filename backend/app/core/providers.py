# app/core/providers.py

from app.repositories.artist_repository import ArtistRepository
from app.services.artist_service import ArtistService
from app.core.dependencies import db_dependency, user_dependency

from app.services import (
    user_services,
    playlist_services,
)

from app.repositories import (
    user_repository,
    playlist_repository
)


def get_user_service(
    user: user_dependency,
    db: db_dependency,
) -> user_services.UserService:
    user_repo = user_repository.UserRepository(db)
    return user_services.UserService(
        user=user, 
        db=db, 
        user_repo=user_repo
    )


def get_playlist_service(
    user: user_dependency,
    db: db_dependency,
) -> playlist_services.PlaylistService:
    
    playlist_repo = playlist_repository.PlaylistRepository(db)
    return playlist_services.PlaylistService(
        user=user,
        db=db,
        playlist_repo=playlist_repo
    )


def get_artist_service(
    user: user_dependency,
    db: db_dependency,
) -> ArtistService:
    
    artist_repo = ArtistRepository(db)
    return ArtistService(user=user, db=db, artist_repo=artist_repo)
