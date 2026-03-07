import sys
import os
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.modules.communities.repository import get_all as get_communities

def verify_maicommunity_leader():
    db = SessionLocal()
    try:
        communities = get_communities(db)
        maicomm = next((c for c in communities if "maicommunity" in c.name_community.lower()), None)
        
        if maicomm:
            print(f"VERIFICATION: Community '{maicomm.name_community}' found.")
            print(f"  Leader Name in API response: {maicomm.leader_name}")
            if maicomm.leader_name:
                print("  SUCCESS: Leader name is now correctly retrieved via role linkage.")
            else:
                print("  STILL MISSING: No user with rol_id=3 and community_id found for this community.")
        else:
            print("VERIFICATION ERROR: MaiCommunity not found in response.")

    finally:
        db.close()

if __name__ == "__main__":
    sys.path.append(os.getcwd())
    verify_maicommunity_leader()
