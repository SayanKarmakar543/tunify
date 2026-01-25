# app/api/v1/artist.py
from fastapi import APIRouter, Depends, status, HTTPException, Query
from typing import Annotated, List, Optional
from uuid import UUID

from app.core.dependencies import db_dependency, user_dependency
from app.repositories.artist_repository import ArtistRepository
from app.services.artist_service import ArtistService
from app.schemas.artist import ArtistResponse
from app.dtos.custom_response_dto import CustomResponseDTO
from app.core.providers import get_artist_service
from fastapi import Request

router = APIRouter(
    prefix="/api/v1",
    tags=["Artists"]
)


# @router.get(
#     "/artists/{artist_id}",
#     response_model=CustomResponseDTO[ArtistResponse],
#     status_code=status.HTTP_200_OK,
#     summary="Get artist by ID",
# )
# async def get_artist_by_id(
#     artist_id: UUID,
#     service: ArtistService = Depends(get_artist_service),
# ):
#     """
#     Retrieve a single artist by UUID.
#     Returns 404 if not found.
#     """
#     artist = await service.read(artist_id)

#     if artist is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Artist not found",
#         )

#     return CustomResponseDTO[ArtistResponse](
#         success=True,
#         message="Artist retrieved successfully",
#         data=artist,
#         status_code=status.HTTP_200_OK,
#     )


# Get all artists
@router.get(
    "/artists",
    response_model=CustomResponseDTO[List[ArtistResponse]],
    status_code=status.HTTP_200_OK,
)
async def get_all_artists(
    artist_service: ArtistService = Depends(get_artist_service),   # <- dependency declared here
    offset: int = Query(0, ge=0),
    limit: int = Query(25, ge=1, le=100),
    name: Optional[str] = Query(None),
):
    # artist_service is now an ArtistService instance (not a tuple)
    # current_user = artist_service.get_user()
    # if not current_user:
    #     # Let the auth dependency normally raise 401/404, but if you want a DTO response:
    #     return CustomResponseDTO[List[ArtistResponse]](
    #         success=False,
    #         message="User not authenticated",
    #         data=[],
    #         error=["User authentication failed"],
    #         error_code="USER_NOT_FOUND",
    #         status_code=401,
    #     )

    filters = {}
    if name:
        filters["name"] = name

    # items = await artist_service.get_artists(offset=offset, limit=limit, filters=filters)

    items, total = await artist_service.list_artists(offset=offset, limit=limit, filters=filters)

    return CustomResponseDTO[List[ArtistResponse]](
        success=True,
        message="Artists fetched",
        data=items,
        total=total,
        status_code=200,
    )

    

# list artists
# @router.get(
#     "/artists",
#     response_model=List[ArtistResponse],
#     status_code=status.HTTP_200_OK,
# )
# async def get_all_artists(
#     user = Depends(user_dependency),
#     db = Depends(db_dependency),
#     offset: int = Query(0, ge=0),
#     limit: int = Query(25, ge=1, le=100),
#     name: Optional[str] = Query(None),
# ):
#     repo = get_artist_repo(db)
#     service = ArtistService(user=user, db=db, artist_repo=repo)
#     filters = {}
#     if name:
#         # basic exact match filter — you can expand to ilike search later
#         filters["name"] = name
#     items, total = await service.list_artists(offset=offset, limit=limit, filters=filters)
#     return items




# get by id
# @router.get(
#     "/artists/{id}",
#     response_model=ArtistResponse,
#     status_code=status.HTTP_200_OK,
# )
# async def get_artist_by_id(
#     id: UUID,
#     user = Depends(user_dependency),
#     db = Depends(db_dependency),
# ):
#     repo = get_artist_repo(db)
#     service = ArtistService(user=user, db=db, artist_repo=repo)
#     artist = await service.get_artist(id)
#     if not artist:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")
#     return artist

# # create
# @router.post(
#     "/artists",
#     response_model=ArtistResponse,
#     status_code=status.HTTP_201_CREATED,
# )
# async def create_artist(
#     payload: ArtistCreate,
#     user = Depends(user_dependency),
#     db = Depends(db_dependency),
# ):
#     repo = get_artist_repo(db)
#     service = ArtistService(user=user, db=db, artist_repo=repo)
#     created = await service.create_artist(payload.dict())
#     return created

# # update
# @router.put(
#     "/artists/{id}",
#     response_model=ArtistResponse,
#     status_code=status.HTTP_200_OK,
# )
# async def update_artist_by_id(
#     id: UUID,
#     payload: ArtistUpdate,
#     user = Depends(user_dependency),
#     db = Depends(db_dependency),
# ):
#     repo = get_artist_repo(db)
#     service = ArtistService(user=user, db=db, artist_repo=repo)
#     updated = await service.update_artist(id, payload.dict(exclude_unset=True))
#     if not updated:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")
#     return updated

# # delete
# @router.delete(
#     "/artists/{id}",
#     status_code=status.HTTP_204_NO_CONTENT,
# )
# async def delete_artist_by_id(
#     id: UUID,
#     user = Depends(user_dependency),
#     db = Depends(db_dependency),
# ):
#     repo = get_artist_repo(db)
#     service = ArtistService(user=user, db=db, artist_repo=repo)
#     deleted = await service.delete_artist(id)
#     if not deleted:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")
#     return None
