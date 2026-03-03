from sqlalchemy.orm import Session
from . import models, schemas


def get_all_technologies(db: Session):
    return db.query(models.Technology).all()


def get_technology_by_id(db: Session, tech_id: int):
    return db.query(models.Technology).filter(models.Technology.id == tech_id).first()


def create_technology(db: Session, tech: schemas.TechnologyCreate):
    db_obj = models.Technology(**tech.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_technology(db: Session, tech_id: int):
    db_obj = get_technology_by_id(db, tech_id)
    if not db_obj:
        return None
    db.delete(db_obj)
    db.commit()
    return db_obj