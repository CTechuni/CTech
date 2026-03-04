from sqlalchemy.orm import Session
from . import repository, schemas

def list_communities(db: Session):
    return repository.get_all_communities(db)

def create_community(db: Session, community: schemas.CommunityCreate):
    return repository.create_community(db, community)

def create_community_with_leader(db: Session, data: schemas.CommunityLeaderCreate):
    from app.modules.users import service as user_service
    from app.modules.users import repository as user_repo
    community = repository.create_community(db, data.community)
    
    # Get leader role by name
    leader_role = user_repo.get_role_by_name(db, "leader")
    if leader_role:
        user_service.update_user(db, data.leader_id, {
            "rol_id": leader_role.id_rol, 
            "community_id": community.id_community
        })
    return community


def assign_user(db: Session, community_id: int, user_id: int):
    return repository.assign_user_to_community(db, community_id, user_id)

def update_community(db: Session, community_id: int, updates: schemas.CommunityUpdate):
    return repository.update_community(db, community_id, updates.dict(exclude_unset=True))

def delete_community(db: Session, community_id: int):
    return repository.delete_community(db, community_id)

