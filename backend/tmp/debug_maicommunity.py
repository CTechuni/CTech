import sys
import os
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.modules.communities.models import Community
from app.modules.users.models import User

def debug_maicommunity():
    db = SessionLocal()
    try:
        # Buscar la comunidad maicommunity (o similar por nombre)
        comm = db.query(Community).filter(Community.name_community.ilike("%maicommunity%")).first()
        if not comm:
            print("Community 'maicommunity' NOT found by name.")
            # Listar todas para estar seguros
            all_comms = db.query(Community).all()
            for c in all_comms:
                print(f"ID: {c.id_community}, Name: {c.name_community}, LeaderID: {c.leader_id}")
            return

        print(f"FOUND Community: {comm.name_community} (ID: {comm.id_community})")
        print(f"leader_id in Community table: {comm.leader_id}")
        
        if comm.leader_id:
            leader = db.query(User).filter(User.id == comm.leader_id).first()
            if leader:
                print(f"Leader USER found: ID {leader.id}, Name: {leader.name_user}, Email: {leader.email}, Role ID: {leader.rol_id}")
            else:
                print(f"Leader ID {comm.leader_id} NOT found in Users table.")
        
        # También buscar usuarios que tengan esta comunidad asignada (aunque el líder se define en community.leader_id)
        members = db.query(User).filter(User.community_id == comm.id_community).all()
        print(f"Total members in this community: {len(members)}")
        for m in members:
            if m.rol_id == 3: # 3 es Leader
                print(f"  User with Leader Role in this community: {m.name_user} (ID: {m.id})")

    finally:
        db.close()

if __name__ == "__main__":
    sys.path.append(os.getcwd())
    debug_maicommunity()
