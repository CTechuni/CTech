from sqlalchemy.orm import Session
from sqlalchemy import func
from app.modules.users.models import User
from . import models, schemas

def get_all(db: Session):
    # Optimized query with joins for members and leader name
    Leader = db.query(User).subquery()
    
    query = db.query(
        models.Community,
        func.count(User.id).label("member_count")
    ).outerjoin(User, User.community_id == models.Community.id_community)\
     .group_by(models.Community.id_community)
    
    results = query.all()
    
    final = []
    for comm, count in results:
        # Simple subquery or separate fetch for leader name to keep it clean
        leader_name = None
        if comm.leader_id:
            leader = db.query(User.name_user).filter(User.id == comm.leader_id).first()
            leader_name = leader[0] if leader else None
        
        comm.member_count = count
        comm.leader_name = leader_name
        final.append(comm)
        
    return final

def get_by_id(db: Session, community_id: int):
    comm = db.query(models.Community).filter(models.Community.id_community == community_id).first()
    if comm:
        # Add dynamic fields for the response schema
        count = db.query(func.count(User.id)).filter(User.community_id == community_id).scalar()
        leader_name = None
        if comm.leader_id:
            leader = db.query(User.name_user).filter(User.id == comm.leader_id).first()
            leader_name = leader[0] if leader else None
            
        comm.member_count = count or 0
        comm.leader_name = leader_name
    return comm

def create(db: Session, community: schemas.CommunityCreate):
    db_community = models.Community(**community.model_dump())
    db.add(db_community)
    db.commit()
    db.refresh(db_community)
    return get_by_id(db, db_community.id_community)

def update(db: Session, community_id: int, data: dict):
    print(f"Updating community {community_id} with data: {data}")
    db.query(models.Community).filter(models.Community.id_community == community_id).update(data)
    db.commit()
    return get_by_id(db, community_id)

def delete(db: Session, community_id: int):
    community = get_by_id(db, community_id)
    if community:
        db.delete(community)
        db.commit()
    return community
    