from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.game_session_repository import GameSessionRepository
from app.exceptions.custom_exceptions import GameSessionNotFoundException, NotOwnerException, GenericException
from app.schemas.game_session import LeaderboardEntry, UserAnalyticsResponse
from sqlalchemy.engine import Row

class GameSessionService:
    def __init__(self, db: AsyncSession):
        self.repository = GameSessionRepository(db)

    async def start_game(self, user_id: int):
        return await self.repository.create_session(user_id)

    async def stop_game(self, session_id: UUID, user_id: int):
        session = await self.repository.stop_session(session_id)
        if not session:
            raise GameSessionNotFoundException()
        if session.user_id != user_id:
            raise NotOwnerException()
        return session
    
    async def get_leaderboard(self, page: int = 1, limit: int = 10) -> list[LeaderboardEntry]:
        offset = (page - 1) * limit
        rows: list[Row] = await self.repository.get_leaderboard(limit=limit, offset=offset)
        return [
            LeaderboardEntry(
                user_id=row.user_id,
                username=row.username,
                total_games=row.total_games,
                avg_deviation=row.avg_deviation,
                best_deviation=row.best_deviation,
            )
            for row in rows
        ]


    async def get_user_analytics(self, user_id: UUID) -> UserAnalyticsResponse:
        try:
            data = await self.repository.get_user_analytics(user_id)
        except GenericException as e:
            raise e
        return UserAnalyticsResponse(**data)