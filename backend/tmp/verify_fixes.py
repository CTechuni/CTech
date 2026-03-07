import sys
import os
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.modules.communities.repository import get_all as get_communities
from app.modules.users.models import User, Profile

def verify_fixes():
    db = SessionLocal()
    try:
        print("--- Verificando Nombres de Líderes ---")
        communities = get_communities(db)
        for comm in communities:
            print(f"Comunidad: {comm.name_community}")
            print(f"  Leader ID: {comm.leader_id}")
            print(f"  Leader Name (Backend Output): {comm.leader_name}")
            if comm.leader_id and not comm.leader_name:
                print("  ERROR: Leader Name is EMPTY despite having an ID!")
            else:
                print("  OK")

        print("\n--- Verificando Vinculación de Perfil ---")
        # Check some users to see if they have profiles
        users = db.query(User).all()
        for u in users:
            profile = db.query(Profile).filter(Profile.user_id == u.id).first()
            if profile:
                print(f"Usuario {u.email}: Perfil VINCULADO")
            else:
                print(f"Usuario {u.email}: Perfil NO ENCONTRADO (Esperado si es un usuario antiguo)")

    finally:
        db.close()

if __name__ == "__main__":
    # Add project root to path
    sys.path.append(os.getcwd())
    verify_fixes()
