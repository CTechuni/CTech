from sqlalchemy.orm import Session
from . import repository, schemas

def list_communities(db: Session):
    return repository.get_all_communities(db)

def create_community(db: Session, community: schemas.CommunityCreate):
    return repository.create_community(db, community)
