from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import UserCreate, UserResponse
from app import crud

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Создать или получить существующего пользователя по Telegram ID"""
    return crud.get_or_create_user(db, user.tg_id)


@router.get("/{tg_id}", response_model=UserResponse)
def get_user(tg_id: int, db: Session = Depends(get_db)):
    """Получить пользователя по Telegram ID"""
    user = crud.get_user_by_tg_id(db, tg_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user