"""FastAPI dependencies for authentication and authorization."""

import logging
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import decode_token
from app.db.models import User
from app.db.session import get_db

logger = logging.getLogger("quantniti.auth")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    auto_error=False,
)


async def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Strict authentication dependency requiring a valid Bearer JWT.

    Raises:
        HTTPException 401: If token is missing, invalid, expired, or user not found.
        HTTPException 403: If user account is inactive.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token:
        raise credentials_exception

    try:
        payload = decode_token(token)
        if payload.get("token_type") != "access":
            raise credentials_exception
        user_id = payload.get("sub")
        if not user_id:
            raise credentials_exception
    except Exception as exc:
        logger.debug(f"JWT decode error: {exc}")
        raise credentials_exception

    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user account",
        )

    return user


async def get_optional_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> Optional[User]:
    """Frictionless guest preview fallback dependency.

    Returns the authenticated User if a valid Bearer token is provided.
    Returns None if no token or an invalid token is provided, allowing
    guest workflows to proceed smoothly without raising an HTTPException.
    """
    if not token:
        return None

    try:
        payload = decode_token(token)
        if payload.get("token_type") != "access":
            return None
        user_id = payload.get("sub")
        if not user_id:
            return None

        stmt = select(User).where(User.id == user_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if user and user.is_active:
            return user
        return None
    except Exception:
        # Silently fall back to guest mode for any invalid/expired token in optional route
        return None
