from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    order = Column(Integer, nullable=False, default=0, index=True)
    is_active = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<Activity(id={self.id}, name='{self.name}', order={self.order})>"