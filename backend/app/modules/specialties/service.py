from sqlalchemy.orm import Session
from . import repository, schemas


def list_specialties(db: Session):
    return repository.get_all_specialties(db)


def create_specialty(db: Session, specialty: schemas.SpecialtyCreate):
    return repository.create_specialty(db, specialty)


def delete_specialty(db: Session, specialty_id: int):
    return repository.delete_specialty(db, specialty_id)
