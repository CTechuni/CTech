from sqlalchemy.orm import Session, joinedload
from . import models


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).options(joinedload(models.User.profile)).filter(models.User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).options(joinedload(models.User.profile)).filter(models.User.id == user_id).first()

def get_all_users(db: Session):
    return db.query(models.User).options(joinedload(models.User.profile)).all()

def get_users_by_role(db: Session, role_name: str):
    return db.query(models.User).options(joinedload(models.User.profile)).join(models.Role).filter(models.Role.name_rol == role_name).all()

def get_role_by_id(db: Session, role_id: int):
    return db.query(models.Role).filter(models.Role.id_rol == role_id).first()

def get_role_by_name(db: Session, role_name: str):
    return db.query(models.Role).filter(models.Role.name_rol == role_name).first()

def create_user(db: Session, user_data: dict):
    db_user = models.User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, updates: dict):
    photo_url = updates.pop("photo_url", None)
    
    if updates:
        db.query(models.User).filter(models.User.id == user_id).update(updates)
    
    if photo_url is not None:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user:
            if user.profile:
                user.profile.photo_url = photo_url
            else:
                new_profile = models.Profile(photo_url=photo_url, email=user.email, full_name=user.name_user)
                db.add(new_profile)
                db.flush()
                user.profile_id = new_profile.id_profile
    
    db.commit()
    return get_user_by_id(db, user_id)

def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if user:
        db.delete(user)
        db.commit()
    return user
