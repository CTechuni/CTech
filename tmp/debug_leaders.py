import sys
import os
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.modules.communities.models import Community
from app.modules.users.models import User

def debug_leaders():
    db = SessionLocal()
    try:
        communities = db.query(Community).all()
        print(f"Total communities: {len(communities)}")
        for comm in communities:
            print(f"\nCommunity: {comm.name_community} (ID: {comm.id_community})")
            print(f"Leader ID: {comm.leader_id}")
            if comm.leader_id:
                leader = db.query(User).filter(User.id == comm.leader_id).first()
                if leader:
                    print(f"Leader found: {leader.name_user} (Email: {leader.email})")
                else:
                    print("Leader NOT found in User table!")
            else:
                print("No leader assigned.")
    finally:
        db.close()

if __name__ == "__main__":
    # Add project root to path
    sys.path.append(os.getcwd())
    debug_leaders()
