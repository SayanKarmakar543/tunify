from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional
from uuid import UUID

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: Optional[str] = "user"
    # profile_image: Optional[str] = Field(default="")
    profile_image: Optional[str] = Field(
        default=None,
        description="Optional profile image URL"
    )

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

    # @field_validator("password")
    # @classmethod
    # def validate_password(cls, v):
    #     if  not any(c.isdigit() for c in v):
    #         raise ValueError("Password must contain at least one digit.")
    #     if not any(c.isupper() for c in v):
    #         raise ValueError("Password must contain at least one uppercase letter.")
    #     if not any(c.islower() for c in v):
    #         raise ValueError("Password must contain at least one lowercase letter.")
    #     return v


class UserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    username: str
    email: str
    role: str
    profile_image: Optional[str]
    created_at: datetime

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
    }

class UserUpdateRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    profile_image: Optional[str] = None
