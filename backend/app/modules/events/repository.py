from sqlalchemy.orm import Session
from . import models, schemas

def get_all_events(db: Session):
    return db.query(models.Event).all()

def get_event_by_id(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id_event == event_id).first()

def create_event(db: Session, event: schemas.EventCreate, user_id: int):
    db_obj = models.Event(**event.dict())
    db_obj.created_by = user_id
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_event(db: Session, event_id: int, event_data: schemas.EventBase):
    db_obj = get_event_by_id(db, event_id)
    if db_obj:
        for key, value in event_data.dict().items():
            setattr(db_obj, key, value)
        db.commit()
        db.refresh(db_obj)
    return db_obj

def delete_event(db: Session, event_id: int):
    db_obj = get_event_by_id(db, event_id)
    if db_obj:
        db.delete(db_obj)
        db.commit()
        return True
    return False

