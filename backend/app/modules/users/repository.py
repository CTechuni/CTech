from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, outerjoin
from . import models
from app.modules.communities.models import Community

def get_all(db: Session):
    return db.query(models.User).options(joinedload(models.User.profile)).all()

def get_by_id(db: Session, user_id: int):
    return db.query(models.User).options(joinedload(models.User.profile)).filter(models.User.id == user_id).first()

def get_by_role(db: Session, role_id: int):
    return db.query(models.User).options(joinedload(models.User.profile)).filter(models.User.rol_id == role_id).all()

def get_leaders_enriched(db: Session):
    """Returns leaders with community_name, community_code and member_count."""
    # Subquery: count members per community
    MemberCount = db.query(
        models.User.community_id,
        func.count(models.User.id).label('member_count')
    ).filter(models.User.community_id != None).group_by(models.User.community_id).subquery()

    results = db.query(
        models.User,
        Community.name_community,
        Community.code.label('community_code'),
        Community.status_community,
        MemberCount.c.member_count
    ).options(joinedload(models.User.profile))\
     .outerjoin(Community, models.User.community_id == Community.id_community)\
     .outerjoin(MemberCount, models.User.community_id == MemberCount.c.community_id)\
     .filter(models.User.rol_id == 3)\
     .all()

    leaders = []
    for user, comm_name, comm_code, comm_status, member_count in results:
        user.community_name = comm_name
        user.community_code = comm_code
        user.community_status = comm_status
        user.member_count = member_count or 0
        leaders.append(user)
    return leaders

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
def get_by_community(db: Session, community_id: int):
    return db.query(models.User).options(joinedload(models.User.profile)).filter(models.User.community_id == community_id).all()
