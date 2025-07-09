from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.game_session import LeaderboardEntry
from uuid import UUID
from sqlalchemy import text
from app.schemas.game_session import GameSessionResponse, UserAnalyticsResponse
from app.core.dependencies import get_db
from app.core.security import get_current_user
from app.services.game_session_service import GameSessionService
from app.exceptions.custom_exceptions import InvalidCredentialsException

router = APIRouter(prefix="/games", tags=["Game"])

@router.post("/start", response_model=GameSessionResponse)
async def start_game(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    service = GameSessionService(db)
    game_session = await service.start_game(user.id)
    return GameSessionResponse.from_orm(game_session)

@router.post("/{session_id}/stop", response_model=GameSessionResponse)
async def stop_game(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    service = GameSessionService(db)
    return await service.stop_game(session_id, user.id)

@router.get("/leaderboard", response_model=list[LeaderboardEntry])
async def get_leaderboard(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    service = GameSessionService(db)
    return await service.get_leaderboard(page=page, limit=limit)

@router.get("/analytics/{user_id}", response_model=UserAnalyticsResponse)
async def get_user_analytics(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if user_id != current_user.id:
        raise InvalidCredentialsException

    service = GameSessionService(db)
    return await service.get_user_analytics(user_id)

@router.post("/dev/load-test-data")
async def load_test_data(db: AsyncSession = Depends(get_db)):
    with open("scripts/test_data.sql", "r") as f:
        raw_sql = f.read()

    statements = raw_sql.split(";")

    for stmt in statements:
        stmt = stmt.strip()
        if stmt:
            await db.execute(text(stmt))

    await db.commit()
    return {"message": "Test data loaded"}