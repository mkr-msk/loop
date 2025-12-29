from sqlalchemy import Column, Integer, BigInteger
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(BigInteger, unique=True, nullable=False, index=True)

    # Связь с сессиями
    sessions = relationship("Session", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, tg_id={self.tg_id})>"