from app.core.database import SessionLocal
from app.modules.users.models import Role, User
from app.modules.communities.models import Community
from sqlalchemy import func

def check_db():
    db = SessionLocal()
    try:
        print("--- ROLES ---")
        roles = db.query(Role).all()
        for r in roles:
            user_count = db.query(User).filter(User.rol_id == r.id_rol).count()
            print(f"ID: {r.id_rol}, Name: {r.name_rol}, Users: {user_count}")
        
        print("\n--- COMMUNITY STATUS ---")
        statuses = db.query(Community.status_community, func.count(Community.id_community)).group_by(Community.status_community).all()
        for status, count in statuses:
            print(f"Status: '{status}', Count: {count}")

        print("\n--- TOTALS ---")
        print(f"Total Users: {db.query(User).count()}")
        print(f"Total Communities: {db.query(Community).count()}")

    finally:
        db.close()

if __name__ == "__main__":
    check_db()
