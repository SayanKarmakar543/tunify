# Password hashing logic

from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from app.core.config import settings
from typing import Optional
from jose import jwt
import uuid


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(email: str, id: uuid.UUID, role: str, expire_delta) -> str:

    """
    Create a JWT access token.

    :param data: Dictionary with data to encode in the token (e.g., user_id, roles)
    :param expires_delta: Optional timedelta for custom token expiry
    :return: Encoded JWT as a string
    """

    encode = {
        "sub": email,
        "id": str(id),
        "role": role.value if hasattr(role, "value") else role
    }

    expires = datetime.now(timezone.utc) + (
        expire_delta if expire_delta else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    encode.update({"exp": expires})

    return jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:

    """
    Create a JWT refresh token.

    :param data: Data (e.g., user_id) to encode in the token
    :param expires_delta: Optional timedelta for custom expiration
    :return: Encoded JWT refresh token as a string
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta if expires_delta else timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
