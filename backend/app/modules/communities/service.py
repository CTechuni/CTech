from sqlalchemy.orm import Session
from . import repository, schemas

def list_communities(db: Session):
    return repository.get_all(db)

def create_community(db: Session, community: schemas.CommunityCreate):
    return repository.create(db, community)

def update_community(db: Session, community_id: int, data: schemas.CommunityUpdate):
    return repository.update(db, community_id, data.model_dump(exclude_unset=True))

def delete_community(db: Session, community_id: int):
    return repository.delete(db, community_id)
    