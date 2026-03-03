from sqlalchemy.orm import Session
from . import models


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_role_by_id(db: Session, role_id: int):
    return db.query(models.Role).filter(models.Role.id_rol == role_id).first()
