from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    start_time = Column(DateTime, nullable=False, default=datetime.now())
    end_time = Column(DateTime, nullable=True)

    # Связи
    activity = relationship("Activity")
    user = relationship("User", back_populates="sessions")

    @property
    def duration(self):
        """Вычисляемая длительность сессии"""
        if self.end_time:
            return self.end_time - self.start_time
        return None

    def __repr__(self):
        return f"<Session(id={self.id}, activity_id={self.activity_id}, user_id={self.user_id})>"