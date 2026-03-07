import sys
import os
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.modules.communities.models import Community
from app.modules.users.models import User

def list_all_leaders_and_comms():
    db = SessionLocal()
    try:
        print("--- COMUNIDADES EN DB ---")
        comms = db.query(Community).all()
        for c in comms:
            print(f"Comm ID: {c.id_community}, Name: {c.name_community}, LeaderID field: {c.leader_id}")
        
        print("\n--- LIDERES (ROL 3) EN DB ---")
        leaders = db.query(User).filter(User.rol_id == 3).all()
        for l in leaders:
            print(f"Leader ID: {l.id}, Name: {l.name_user}, Email: {l.email}, Assigned Comm ID: {l.community_id}")

    finally:
        db.close()

if __name__ == "__main__":
    sys.path.append(os.getcwd())
    list_all_leaders_and_comms()
