from pydantic import BaseModel, UUID4, ConfigDict
from typing import Optional, List
from datetime import datetime

class GameSessionResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    start_time: datetime
    stop_time: Optional[datetime]
    duration_ms: Optional[float] = None
    deviation_ms: Optional[float] = None
    status: str

    model_config = ConfigDict(from_attributes=True)

class LeaderboardEntry(BaseModel):
    user_id: UUID4
    username: str
    total_games: int
    avg_deviation: float
    best_deviation: float

    class Config:
        from_attributes = True

class GameSessionSummary(BaseModel):
    session_id: UUID4
    start_time: datetime
    stop_time: Optional[datetime]
    duration_ms: Optional[float]
    deviation_ms: Optional[float]
    status: str

class UserAnalyticsResponse(BaseModel):
    user_id: UUID4
    total_games: int
    avg_deviation: Optional[float]
    best_deviation: Optional[float]
    worst_deviation: Optional[float]
    sessions: List[GameSessionSummary]
