from sqlalchemy.orm import Session
from . import models, schemas


def get_all_specialties(db: Session):
    return db.query(models.Specialty).all()


def get_specialty_by_id(db: Session, specialty_id: int):
    return db.query(models.Specialty).filter(models.Specialty.id == specialty_id).first()


def create_specialty(db: Session, specialty: schemas.SpecialtyCreate):
    db_obj = models.Specialty(**specialty.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_specialty(db: Session, specialty_id: int):
    db_obj = get_specialty_by_id(db, specialty_id)
    if not db_obj:
        return None
    db.delete(db_obj)
    db.commit()
    return db_obj
