from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from fastapi import Depends
from app.repositories.game_session_repository import GameSessionRepository
from app.services.game_session_service import GameSessionService

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def get_game_session_service(db: AsyncSession = Depends(get_db)) -> GameSessionService:
    repository = GameSessionRepository(db)
    return GameSessionService(repository)