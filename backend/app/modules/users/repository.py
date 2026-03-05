from sqlalchemy.orm import Session
from . import models

def get_all(db: Session):
    return db.query(models.User).all()

def get_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_by_role(db: Session, role_id: int):
    return db.query(models.User).filter(models.User.rol_id == role_id).all()

def update(db: Session, user_id: int, data: dict):
    db.query(models.User).filter(models.User.id == user_id).update(data)
    db.commit()
    return get_by_id(db, user_id)

def delete(db: Session, user_id: int):
    user = get_by_id(db, user_id)
    if user:
        db.delete(user)
        db.commit()
    return user
