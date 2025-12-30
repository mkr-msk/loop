from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import ActivityCreate, ActivityUpdate, ActivityResponse, ActivityOrderUpdate
from app import crud

router = APIRouter(prefix="/activities", tags=["activities"])


@router.get("/", response_model=List[ActivityResponse])
def list_activities(db: Session = Depends(get_db)):
    """Получить все активности"""
    return crud.get_activities(db)


@router.get("/{activity_id}", response_model=ActivityResponse)
def get_activity(activity_id: int, db: Session = Depends(get_db)):
    """Получить активность по ID"""
    activity = crud.get_activity(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.post("/", response_model=ActivityResponse)
def create_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
    """Создать новую активность"""
    return crud.create_activity(db, activity)


@router.patch("/{activity_id}", response_model=ActivityResponse)
def update_activity(activity_id: int, activity: ActivityUpdate, db: Session = Depends(get_db)):
    """Обновить активность"""
    db_activity = crud.update_activity(db, activity_id, activity)
    if not db_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return db_activity


@router.delete("/{activity_id}")
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    """Удалить активность"""
    success = crud.delete_activity(db, activity_id)
    if not success:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"message": "Activity deleted successfully"}


@router.post("/reorder")
def reorder_activities(order_data: ActivityOrderUpdate, db: Session = Depends(get_db)):
    """Обновить порядок активностей"""
    crud.update_activities_order(db, order_data.activity_ids)
    return {"message": "Order updated successfully"}