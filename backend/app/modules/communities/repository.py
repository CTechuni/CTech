from sqlalchemy.orm import Session
from . import models, schemas

def get_all(db: Session):
    return db.query(models.Community).all()

def get_by_id(db: Session, community_id: int):
    return db.query(models.Community).filter(models.Community.id_community == community_id).first()

def create(db: Session, community: schemas.CommunityCreate):
    db_community = models.Community(**community.model_dump())
    db.add(db_community)
    db.commit()
    db.refresh(db_community)
    return db_community

def update(db: Session, community_id: int, data: dict):
    db.query(models.Community).filter(models.Community.id_community == community_id).update(data)
    db.commit()
    return get_by_id(db, community_id)

def delete(db: Session, community_id: int):
    community = get_by_id(db, community_id)
    if community:
        db.delete(community)
        db.commit()
    return community
    