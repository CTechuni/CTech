from sqlalchemy.orm import Session
from . import repository, schemas

def list_events(db: Session):
    return repository.get_all_events(db)

def create_event(db: Session, event: schemas.EventCreate, user_id: int):
    if event.capacity < 0:
        raise ValueError("La capacidad no puede ser negativa")
    return repository.create_event(db, event, user_id)

def update_event(db: Session, event_id: int, event_data: schemas.EventBase):
    db_event = repository.get_event_by_id(db, event_id)
    if not db_event:
        return None
    return repository.update_event(db, event_id, event_data)

def delete_event(db: Session, event_id: int):
    return repository.delete_event(db, event_id)

