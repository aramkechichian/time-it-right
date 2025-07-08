from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, func
from sqlalchemy.orm import aliased
from sqlalchemy.engine import Row
from app.models.game_session import GameSession
from app.models.user import User
from uuid import UUID
from datetime import datetime, timedelta
from app.exceptions.custom_exceptions import SessionExpiredException


class GameSessionRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_session(self, user_id: int) -> GameSession:
        game_session = GameSession(user_id=user_id, status="started", start_time=datetime.utcnow())
        self.session.add(game_session)
        await self.session.commit()
        await self.session.refresh(game_session)
        return game_session

    async def stop_session(self, session_id: UUID) -> GameSession | None:
        query = await self.session.execute(
            select(GameSession).where(GameSession.id == session_id)
        )
        game_session = query.scalar_one_or_none()

        # Si no existe o ya fue detenida
        if not game_session or game_session.status != "started":
            return None

        # Verificar si la sesión expiró (más de 30 minutos desde que se inició)
        if datetime.utcnow() - game_session.start_time > timedelta(minutes=30):
            game_session.status = "expired"
            await self.session.commit()
            raise SessionExpiredException()

        # Calcular duración y desviación
        game_session.stop_time = datetime.utcnow()
        game_session.duration_ms = (game_session.stop_time - game_session.start_time).total_seconds() * 1000
        game_session.deviation_ms = abs(10000 - game_session.duration_ms)
        game_session.status = "completed"

        await self.session.commit()
        await self.session.refresh(game_session)
        return game_session

    async def get_session(self, session_id: UUID) -> GameSession | None:
        query = await self.session.execute(select(GameSession).where(GameSession.id == session_id))
        return query.scalar_one_or_none()


    async def get_leaderboard(self, limit: int = 10, offset: int = 0) -> list[Row]:
        # Filters only "completed" sessions
        # Groups by user_id and username
        # Calculates total games, average deviation, and best attempt
        # Applies limit and offset for pagination        
        UserAlias = aliased(User)

        result = await self.session.execute(
            select(
                GameSession.user_id,
                UserAlias.username,
                func.count(GameSession.id).label("total_games"),
                func.avg(GameSession.deviation_ms).label("avg_deviation"),
                func.min(GameSession.deviation_ms).label("best_deviation")
            )
            .join(UserAlias, GameSession.user_id == UserAlias.id)
            .where(GameSession.status == "completed")
            .group_by(GameSession.user_id, UserAlias.username)
            .order_by(func.avg(GameSession.deviation_ms).asc())
            .limit(limit)
            .offset(offset)
        )
        return result.all()
    

    async def get_user_analytics(self, user_id: UUID) -> dict:
        # 1. Métricas agregadas
        stmt_summary = (
            select(
                func.count(GameSession.id).label("total_games"),
                func.avg(GameSession.deviation_ms).label("avg_deviation"),
                func.min(GameSession.deviation_ms).label("best_deviation"),
                func.max(GameSession.deviation_ms).label("worst_deviation"),
            )
            .where(GameSession.user_id == user_id)
            .where(GameSession.status == "completed")
        )
        result = await self.session.execute(stmt_summary)
        summary = result.one()

        # 2. Lista de sesiones del usuario
        stmt_sessions = (
            select(
                GameSession.id,
                GameSession.start_time,
                GameSession.stop_time,
                GameSession.duration_ms,
                GameSession.deviation_ms,
                GameSession.status,
            )
            .where(GameSession.user_id == user_id)
            .order_by(GameSession.start_time.desc())
        )
        result = await self.session.execute(stmt_sessions)
        sessions = result.fetchall()

        session_list = [
            {
                "session_id": str(row.id),
                "start_time": row.start_time,
                "stop_time": row.stop_time,
                "duration_ms": row.duration_ms,
                "deviation_ms": row.deviation_ms,
                "status": row.status,
            }
            for row in sessions
        ]

        return {
            "user_id": str(user_id),
            "total_games": summary.total_games or 0,
            "avg_deviation": float(summary.avg_deviation) if summary.avg_deviation is not None else None,
            "best_deviation": float(summary.best_deviation) if summary.best_deviation is not None else None,
            "worst_deviation": float(summary.worst_deviation) if summary.worst_deviation is not None else None,
            "sessions": session_list
        }