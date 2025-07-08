import pytest
import asyncio
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.game_session_service import GameSessionService
from app.exceptions.custom_exceptions import GameSessionNotFoundException, NotOwnerException, GenericException
from app.schemas.game_session import LeaderboardEntry, UserAnalyticsResponse


@patch("app.services.game_session_service.GameSessionRepository")
def test_start_game(mock_repo_class):
    mock_repo = AsyncMock()
    mock_repo.create_session.return_value = MagicMock()
    mock_repo_class.return_value = mock_repo

    db = MagicMock()
    service = GameSessionService(db)
    result = asyncio.run(service.start_game(user_id=1))

    assert result is not None
    mock_repo.create_session.assert_awaited_once()


@patch("app.services.game_session_service.GameSessionRepository")
def test_stop_game_success(mock_repo_class):
    session = MagicMock()
    session.user_id = 123

    mock_repo = AsyncMock()
    mock_repo.stop_session.return_value = session
    mock_repo_class.return_value = mock_repo

    db = MagicMock()
    service = GameSessionService(db)
    result = asyncio.run(service.stop_game(session_id=uuid4(), user_id=123))

    assert result == session


@patch("app.services.game_session_service.GameSessionRepository")
def test_stop_game_not_found(mock_repo_class):
    mock_repo = AsyncMock()
    mock_repo.stop_session.return_value = None
    mock_repo_class.return_value = mock_repo

    db = MagicMock()
    service = GameSessionService(db)

    with pytest.raises(GameSessionNotFoundException):
        asyncio.run(service.stop_game(session_id=uuid4(), user_id=1))


@patch("app.services.game_session_service.GameSessionRepository")
def test_stop_game_not_owner(mock_repo_class):
    session = MagicMock()
    session.user_id = 999

    mock_repo = AsyncMock()
    mock_repo.stop_session.return_value = session
    mock_repo_class.return_value = mock_repo

    db = MagicMock()
    service = GameSessionService(db)

    with pytest.raises(NotOwnerException):
        asyncio.run(service.stop_game(session_id=uuid4(), user_id=1))


@patch("app.services.game_session_service.GameSessionRepository")
def test_get_leaderboard(mock_repo_class):
    row = MagicMock()
    row.user_id = uuid4()  # FIX: debe ser UUID
    row.username = "user"
    row.total_games = 10
    row.avg_deviation = 20.0
    row.best_deviation = 5.0

    mock_repo = AsyncMock()
    mock_repo.get_leaderboard.return_value = [row]
    mock_repo_class.return_value = mock_repo

    db = MagicMock()
    service = GameSessionService(db)
    leaderboard = asyncio.run(service.get_leaderboard(page=1, limit=10))

    assert isinstance(leaderboard[0], LeaderboardEntry)
    assert leaderboard[0].user_id == row.user_id


@patch("app.services.game_session_service.GameSessionRepository")
def test_get_user_analytics_success(mock_repo_class):
    fake_data = {
        "user_id": str(uuid4()),
        "total_games": 10,
        "average_duration_ms": 1000.0,
        "average_deviation_ms": 15.0,
        "avg_deviation": 15.0,           # FIX: agregado
        "best_deviation": 5.0,           # FIX: agregado
        "worst_deviation": 30.0,         # FIX: agregado
        "sessions": [],                  # FIX: agregado
        "games": []
    }

    mock_repo = AsyncMock()
    mock_repo.get_user_analytics.return_value = fake_data
    mock_repo_class.return_value = mock_repo

    db = MagicMock()
    service = GameSessionService(db)
    analytics = asyncio.run(service.get_user_analytics(user_id=uuid4()))

    assert isinstance(analytics, UserAnalyticsResponse)
    assert analytics.total_games == 10


@patch("app.services.game_session_service.GameSessionRepository")
def test_get_user_analytics_exception(mock_repo_class):
    mock_repo = AsyncMock()
    mock_repo.get_user_analytics.side_effect = GenericException("Something went wrong")  # FIX: mensaje requerido
    mock_repo_class.return_value = mock_repo

    db = MagicMock()
    service = GameSessionService(db)

    with pytest.raises(GenericException):
        asyncio.run(service.get_user_analytics(user_id=uuid4()))
