# app/utils/response.py
from typing import Optional, List, Any
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.dtos.custom_response_dto import CustomResponseDTO

def create_custom_response(
    *,
    success: bool,
    message: Optional[str] = None,
    data: Optional[Any] = None,
    errors: Optional[List[str]] = None,
    error_code: Optional[str] = None,
    status_code: int,
    total: Optional[int] = None
):
    response = CustomResponseDTO(
        success=success,
        message=message,
        data=data,
        errors=errors,
        error_code=error_code,
        status_code=status_code,
        total=total,
    )

    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(response)
    )
