from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.repositories.user_repository import (
    get_user_by_email,
    get_user_by_username,
    get_user_by_username_or_email,
    create_user,
)
from app.core.security import get_password_hash, verify_password, create_access_token


async def register_user(db: AsyncSession, request: RegisterRequest) -> TokenResponse:
    if await get_user_by_username(db, request.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    if await get_user_by_email(db, request.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(request.password)
    user = await create_user(db, request.username, request.email, hashed_password)

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token)


async def login_user(db: AsyncSession, request: LoginRequest) -> TokenResponse:
    user = await get_user_by_username_or_email(db, request.username_or_email)
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token)
