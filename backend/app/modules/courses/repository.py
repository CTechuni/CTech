from sqlalchemy.orm import Session
from . import models, schemas

def get_all_courses(db: Session):
    return db.query(models.Course).all()

def get_course_by_id(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.id == course_id).first()

def create_course(db: Session, course: schemas.CourseCreate):
    db_obj = models.Course(**course.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_course(db: Session, course_id: int, updates: dict):
    db.query(models.Course).filter(models.Course.id == course_id).update(updates)
    db.commit()
    return get_course_by_id(db, course_id)

def delete_course(db: Session, course_id: int):
    course = get_course_by_id(db, course_id)
    if course:
        db.delete(course)
        db.commit()
    return course
