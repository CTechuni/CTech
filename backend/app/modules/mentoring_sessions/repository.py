from sqlalchemy.orm import Session
from . import models, schemas

def create_session(db: Session, session_data: schemas.SessionCreate):
    db_obj = models.MentoringSession(**session_data.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def list_sessions_by_course(db: Session, course_id: int):
    return db.query(models.MentoringSession).filter(models.MentoringSession.course_id == course_id).all()

def reserve_session(db: Session, session_id: int, student_id: int):
    session = db.query(models.MentoringSession).filter(models.MentoringSession.id == session_id).first()
    if session and session.is_available:
        session.is_available = False
        session.student_id = student_id
        db.commit()
        db.refresh(session)
        return session
    return None

def cancel_session(db: Session, session_id: int):
    session = db.query(models.MentoringSession).filter(models.MentoringSession.id == session_id).first()
    if session:
        session.is_available = True
        session.student_id = None
        db.commit()
        db.refresh(session)
        return session
    return None
