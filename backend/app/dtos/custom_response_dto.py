# app/dtos/custom_response_dto.py
from typing import TypeVar, Generic, Optional, List
from pydantic import BaseModel

T = TypeVar("T")

class CustomResponseDTO(BaseModel, Generic[T]):
    success: bool
    message: Optional[str] = None
    data: Optional[T] = None
    errors: Optional[List[str]] = None
    error_code: Optional[str] = None
    status_code: Optional[int] = None
    total: Optional[int] = None
