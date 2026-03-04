from sqlalchemy.orm import Session
from . import repository, schemas

def create_session(db: Session, session_data: schemas.SessionCreate):
    return repository.create_session(db, session_data)

def list_sessions_by_course(db: Session, course_id: int):
    return repository.list_sessions_by_course(db, course_id)

def reserve_session(db: Session, session_id: int, student_id: int):
    return repository.reserve_session(db, session_id, student_id)

def cancel_session(db: Session, session_id: int):
    return repository.cancel_session(db, session_id)
