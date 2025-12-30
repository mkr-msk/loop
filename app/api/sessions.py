from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import SessionCreate, SessionResponse, SessionWithActivity
from app import crud

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("/start", response_model=SessionResponse)
def start_session(session_data: SessionCreate, db: Session = Depends(get_db)):
    """Начать новую сессию"""
    new_session, error = crud.start_session(db, session_data.user_id)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return new_session


@router.post("/stop", response_model=SessionResponse)
def stop_session(session_data: SessionCreate, db: Session = Depends(get_db)):
    """Завершить текущую сессию"""
    stopped_session, error = crud.stop_session(db, session_data.user_id)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return stopped_session


@router.post("/next", response_model=SessionResponse)
def next_session(session_data: SessionCreate, db: Session = Depends(get_db)):
    """Завершить текущую и начать следующую сессию"""
    new_session, error = crud.next_session(db, session_data.user_id)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return new_session


@router.get("/current/{user_id}", response_model=SessionWithActivity)
def get_current_session(user_id: int, db: Session = Depends(get_db)):
    """Получить текущую активную сессию пользователя"""
    current = crud.get_current_session(db, user_id)
    if not current:
        raise HTTPException(status_code=404, detail="Нет активной сессии")
    return current


@router.get("/history/{user_id}", response_model=List[SessionWithActivity])
def get_session_history(user_id: int, db: Session = Depends(get_db)):
    """Получить историю сессий пользователя"""
    return crud.get_user_sessions(db, user_id)