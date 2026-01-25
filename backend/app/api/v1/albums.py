from fastapi import APIRouter, Depends, status
from app.core.dependencies import db_dependency, user_dependency
from typing import Annotated
from uuid import UUID


router = APIRouter(
    prefix="/api/v1",
    tags=["Albums"]
)


@router.get(
    "/albums",
    status_code=status.HTTP_200_OK,
)
async def get_albums(
    user: user_dependency,
    db: db_dependency,
):
    pass


@router.get(
    "/albums/{id}",
    status_code=status.HTTP_200_OK,
)
async def get_album_by_id(
    id: UUID,
    user: user_dependency,
    db: db_dependency,
):
    pass


@router.post(
    "/albums",
    status_code=status.HTTP_201_CREATED,
)
async def create_album(
    user: user_dependency,
    db: db_dependency,
):
    pass


@router.put(
    "/albums/{id}",
    status_code=status.HTTP_200_OK,
)
async def update_album(
    id: UUID,
    user: user_dependency,
    db: db_dependency,
):
    pass


@router.delete(
    "/albums/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_album(
    id: UUID,
    user: user_dependency,
    db: db_dependency,
):
    pass
