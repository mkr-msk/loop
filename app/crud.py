from sqlalchemy.orm import Session as Session_db
from app.models import Activity, Session, User
from app.schemas import ActivityCreate, ActivityUpdate


def get_activities(db: Session_db):
    return db.query(Activity).order_by(Activity.order).all()


def get_activity(db: Session_db, activity_id: int):
    return db.query(Activity).filter(Activity.id == activity_id).first()


def create_activity(db: Session_db, activity: ActivityCreate):
    db_activity = Activity(**activity.model_dump())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity


def update_activity(db: Session_db, activity_id: int, activity: ActivityUpdate):
    db_activity = get_activity(db, activity_id)
    if not db_activity:
        return None
    
    update_data = activity.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_activity, key, value)

    db.commit()
    db.refresh(db_activity)
    return db_activity


def delete_activity(db: Session_db, activity_id: int):
    db_activity = get_activity(db, activity_id)
    if not db_activity:
        return False
    
    db.delete(db_activity)
    db.commit()
    return True


def update_activities_order(db: Session_db, activity_ids: list[int]):
    for index, activity_id in enumerate(activity_ids):
        db_activity = get_activity(db, activity_id)
        if db_activity:
            db_activity.order = index
    
    db.commit()
    return True


# Session CRUD

def get_current_session(db: Session_db, user_id: int):
    """Получить текущую открытую сессию пользователя"""
    return db.query(Session).filter(
        Session.user_id == user_id,
        Session.end_time is None
    ).first()


def get_last_closed_session(db: Session_db, user_id: int):
    """Получить последнюю закрытую сессию пользователя"""
    return db.query(Session).filter(
        Session.user_id == user_id,
        Session.end_time is not None
    ).order_by(Session.start_time.desc()).first()


def get_next_activity(db: Session_db, user_id: int):
    """Получить следующую активную активность по циклу для пользователя"""
    # Получаем все активные активности по порядку
    active_activities = db.query(Activity).filter(Activity.is_active).order_by(Activity.order).all()
    
    if not active_activities:
        return None
    
    # Сначала проверяем открытую сессию
    current_session = get_current_session(db, user_id)
    if current_session:
        current_activity_id = current_session.activity_id
    else:
        # Если нет открытой, берем последнюю закрытую
        last_session = get_last_closed_session(db, user_id)
        if last_session:
            current_activity_id = last_session.activity_id
        else:
            # Нет ни одной сессии - возвращаем первую активность
            return active_activities[0]
    
    # Находим индекс текущей активности
    current_index = None
    for i, activity in enumerate(active_activities):
        if activity.id == current_activity_id:
            current_index = i
            break
    
    # Если текущая активность была деактивирована - начинаем с первой
    if current_index is None:
        return active_activities[0]
    
    # Берём следующую (или первую, если это была последняя) - цикл
    next_index = (current_index + 1) % len(active_activities)
    return active_activities[next_index]


def start_session(db: Session_db, user_id: int):
    """Начать новую сессию"""
    from datetime import datetime
    from app.models.session import Session as SessionModel
    
    # Проверяем, нет ли открытой сессии
    current = get_current_session(db, user_id)
    if current:
        return None, "Завершите текущую сессию перед началом новой"
    
    # Находим следующую активность
    next_activity = get_next_activity(db, user_id)
    
    if not next_activity:
        return None, "Нет активных активностей"
    
    # Создаём новую сессию
    now = datetime.now()
    new_session = SessionModel(
        user_id=user_id,
        activity_id=next_activity.id,
        start_time=now,
        date=now,
        end_time=None
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    
    return new_session, None


def stop_session(db: Session_db, user_id: int):
    """Завершить текущую сессию"""
    from datetime import datetime
    
    # Находим открытую сессию
    current = get_current_session(db, user_id)
    if not current:
        return None, "Нет активной сессии"
    
    # Закрываем сессию
    current.end_time = datetime.now()
    db.commit()
    db.refresh(current)
    
    return current, None


def next_session(db: Session_db, user_id: int):
    """Завершить текущую и начать следующую"""
    # Останавливаем текущую
    stopped, error = stop_session(db, user_id)
    if error:
        return None, error
    
    # Начинаем новую
    started, error = start_session(db, user_id)
    if error:
        return None, error
    
    return started, None


def get_user_sessions(db: Session_db, user_id: int):
    """Получить историю сессий пользователя"""
    return db.query(Session).filter(
        Session.user_id == user_id
    ).order_by(Session.start_time.desc()).all()


def get_user_by_tg_id(db: Session_db, tg_id: int):
    """Получить пользователя по Telegram ID"""
    return db.query(User).filter(User.tg_id == tg_id).first()


def create_user(db: Session_db, tg_id: int):
    """Создать нового пользователя"""
    db_user = User(tg_id=tg_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_or_create_user(db: Session_db, tg_id: int):
    """Получить существующего или создать нового пользователя"""
    user = get_user_by_tg_id(db, tg_id)
    if not user:
        user = create_user(db, tg_id)
    return user