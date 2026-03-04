from sqlalchemy.orm import Session
from . import models, schemas

def get_all_communities(db: Session):
    return db.query(models.Community).all()

def get_community_by_id(db: Session, community_id: int):
    return db.query(models.Community).filter(models.Community.id_community == community_id).first()

def create_community(db: Session, community: schemas.CommunityCreate):
    db_obj = models.Community(**community.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_community(db: Session, community_id: int, updates: dict):
    db.query(models.Community).filter(models.Community.id_community == community_id).update(updates)
    db.commit()
    return get_community_by_id(db, community_id)

def delete_community(db: Session, community_id: int):
    community = get_community_by_id(db, community_id)
    if community:
        db.delete(community)
        db.commit()
    return community

def assign_user_to_community(db: Session, community_id: int, user_id: int):
    from app.modules.users.models import User
    db.query(User).filter(User.id == user_id).update({"community_id": community_id})
    db.commit()
    return True
