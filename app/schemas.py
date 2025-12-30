from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class ActivityBase(BaseModel):
    name: str
    order: int = 0
    is_active: bool = True


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseModel):
    name: Optional[str] = None
    order: Optional[int] = None
    is_active: Optional[bool] = None


class ActivityResponse(ActivityBase):
    id: int

    class Config:
        from_attributes = True


class ActivityOrderUpdate(BaseModel):
    activity_ids: list[int]


# Session schemas
class SessionBase(BaseModel):
    user_id: int
    activity_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    date: datetime


class SessionCreate(BaseModel):
    user_id: int


class SessionResponse(SessionBase):
    id: int
    
    class Config:
        from_attributes = True


class SessionWithActivity(SessionResponse):
    activity: ActivityResponse


# User schemas
class UserBase(BaseModel):
    tg_id: int


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True