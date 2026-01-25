from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import status

from app.dtos.custom_response_dto import CustomResponseDTO
from app.core.exceptions.domain_exception import (
    ConflictException,
    NotFoundException,
    PermissionDeniedException,
    ValidationException,
    DomainException,
)


def register_exception_handlers(app):

    @app.exception_handler(ConflictException)
    async def conflict_handler(_: Request, exc: ConflictException):
        response = CustomResponseDTO(
            success=False,
            message="Conflict occurred",
            errors=[exc.message],
            error_code="CONFLICT_ERROR",
            status_code=status.HTTP_409_CONFLICT,
        )

        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=response.model_dump(),
        )

    @app.exception_handler(NotFoundException)
    async def not_found_handler(_: Request, exc: NotFoundException):
        response = CustomResponseDTO(
            success=False,
            message="Resource not found",
            errors=[exc.message],
            error_code="NOT_FOUND_ERROR",
            status_code=status.HTTP_404_NOT_FOUND,
        )

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=response.model_dump(),
        )

    @app.exception_handler(PermissionDeniedException)
    async def permission_handler(_: Request, exc: PermissionDeniedException):
        response = CustomResponseDTO(
            success=False,
            message="Permission denied",
            errors=[exc.message],
            error_code="PERMISSION_DENIED_ERROR",
            status_code=status.HTTP_403_FORBIDDEN,
        )

        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=response.model_dump(),
        )

    @app.exception_handler(ValidationException)
    async def validation_handler(_: Request, exc: ValidationException):
        response = CustomResponseDTO(
            success=False,
            message="Validation failed",
            errors=[exc.message],
            error_code="VALIDATION_ERROR",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response.model_dump(),
        )
    
    @app.exception_handler(DomainException)
    async def domain_exception_handler(_: Request, exc: DomainException):
        response_dto = CustomResponseDTO(
            success=False,
            message="Domain error occurred",
            errors=[exc.message],
            error_code="DOMAIN_ERROR",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response_dto.model_dump(),
        )

        