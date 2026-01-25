from fastapi import APIRouter, Depends, HTTPException, status, Depends
from app.schemas.user_schema import UserRequest, UserResponse
from app.core.dependencies import db_dependency, user_dependency
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app.schemas.auth import LoginResponse
from app.repositories.auth_repository import (
    register_repo,
    user_login_repo,
    get_user_details_repo,
)


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"]
)


@router.post(
    "/register", 
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse
)
async def register(
    db: db_dependency, 
    user_request: UserRequest
) -> UserResponse:
    """
    Register a new user.

    :param db: Database session dependency
    :param user_request: User registration data
    :return: Registered user data
    """
    new_user = await register_repo(db, user_request)
    return new_user


@router.post(
    "/login", 
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency
) -> UserResponse:
    
    """
    User login endpoint.

    :param db: Database session dependency
    :param form_data: OAuth2 form data containing username and password
    :return: Logged in user data with access token
    """
    login_response = await user_login_repo(db, form_data.username, form_data.password)
    return login_response


@router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
async def refresh_token(
    db: db_dependency,
    user_request: UserRequest
):
    pass


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    user: user_dependency
):
    pass


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse
)
async def get_user_details(
    user: user_dependency,
    db: db_dependency
):
    user_details = await get_user_details_repo(user, db)
    return user_details
