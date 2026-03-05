from typing import Optional  # <-- Esta es la importación que soluciona el NameError
from sqlalchemy.orm import Session
from . import models

def get_by_course(db: Session, course_id: int):
    """Obtiene sesiones disponibles para un curso específico."""
    return db.query(models.MentoringSession).filter(
        models.MentoringSession.course_id == course_id,
        models.MentoringSession.status == "available"
    ).all()

def create(db: Session, session_dict: dict):
    """Crea una nueva sesión de mentoría."""
    db_session = models.MentoringSession(**session_dict)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def update_status(db: Session, session_id: int, student_id: Optional[int], status: str):
    """
    Actualiza el estado y asigna un estudiante (el cual puede ser None/Nulo
    si la sesión se libera o se cancela).
    """
    db_session = db.query(models.MentoringSession).filter(
        models.MentoringSession.id == session_id
    ).first()
    
    if db_session:
        db_session.student_id = student_id
        db_session.status = status
        db.commit()
        db.refresh(db_session)
    return db_session
    