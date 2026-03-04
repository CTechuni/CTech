from sqlalchemy.orm import Session
from . import models, schemas

def get_all_events(db: Session):
    return db.query(models.Event).all()

def create_event(db: Session, event: schemas.EventCreate, user_id: int):
    db_obj = models.Event(**event.dict())
    db_obj.created_by = user_id
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
