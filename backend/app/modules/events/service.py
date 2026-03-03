from sqlalchemy.orm import Session
from . import repository, schemas

def list_events(db: Session):
    return repository.get_all_events(db)

def create_event(db: Session, event: schemas.EventCreate):
    # Aqui se podrian anadir validaciones de negocio (ej: fecha futura)
    return repository.create_event(db, event)
