import pytest
from uuid import uuid4
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.routes.game_session_routes import get_current_user

client = TestClient(app)

# 💡 Fixture para inyectar un mock de usuario autenticado
@pytest.fixture(autouse=True)
def override_current_user():
    mock_user = AsyncMock()
    mock_user.id = uuid4()
    app.dependency_overrides[get_current_user] = lambda: mock_user
    yield
    app.dependency_overrides.clear()


@patch("app.routes.game_session_routes.GameSessionService")
def test_start_game(mock_service_class):
    mock_game = AsyncMock()
    mock_game.id = uuid4()
    mock_game.user_id = uuid4()
    mock_game.start_time = "2024-01-01T00:00:00Z"
    mock_game.stop_time = None
    mock_game.duration_ms = None
    mock_game.deviation_ms = None
    mock_game.status = "in_progress"

    mock_service = AsyncMock()
    mock_service.start_game.return_value = mock_game
    mock_service_class.return_value = mock_service

    response = client.post("/games/start")
    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"


@patch("app.routes.game_session_routes.GameSessionService")
def test_stop_game(mock_service_class):
    session_id = uuid4()

    mock_game = AsyncMock()
    mock_game.id = session_id
    mock_game.user_id = uuid4()
    mock_game.start_time = "2024-01-01T00:00:00Z"
    mock_game.stop_time = "2024-01-01T00:00:10Z"
    mock_game.duration_ms = 10000
    mock_game.deviation_ms = 15
    mock_game.status = "finished"

    mock_service = AsyncMock()
    mock_service.stop_game.return_value = mock_game
    mock_service_class.return_value = mock_service

    response = client.post(f"/games/{session_id}/stop")
    assert response.status_code == 200
    assert response.json()["status"] == "finished"


@patch("app.routes.game_session_routes.GameSessionService")
def test_get_leaderboard(mock_service_class):
    mock_service = AsyncMock()
    fake_leaderboard = [
        {
            "user_id": str(uuid4()),
            "username": "player1",
            "total_games": 5,
            "avg_deviation": 100.5,
            "best_deviation": 20.0
        }
    ]
    mock_service.get_leaderboard.return_value = fake_leaderboard
    mock_service_class.return_value = mock_service

    response = client.get("/games/leaderboard?page=1&limit=10")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["username"] == "player1"

