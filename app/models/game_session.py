import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from app.models.base import Base

class GameStatus(str, enum.Enum):
    started = "started"
    completed = "completed"
    expired = "expired"

class GameSession(Base):
    __tablename__ = "game_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    stop_time = Column(DateTime, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    deviation_ms = Column(Integer, nullable=True)
    status = Column(Enum(GameStatus), nullable=False, default=GameStatus.started)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="game_sessions")
