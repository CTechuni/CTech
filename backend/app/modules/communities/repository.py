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
