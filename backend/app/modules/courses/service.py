from sqlalchemy.orm import Session
from . import repository, schemas

def list_courses(db: Session):
    return repository.get_all_courses(db)

def get_course(db: Session, course_id: int):
    return repository.get_course_by_id(db, course_id)

def create_course(db: Session, course: schemas.CourseCreate):
    return repository.create_course(db, course)

def update_course(db: Session, course_id: int, updates: schemas.CourseUpdate):
    return repository.update_course(db, course_id, updates.dict(exclude_unset=True))

def delete_course(db: Session, course_id: int):
    return repository.delete_course(db, course_id)
