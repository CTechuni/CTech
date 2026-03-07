from app.core.database import SessionLocal
from app.modules.users.models import User
from app.modules.courses.models import Course
from app.modules.communities.models import Community
from app.modules.events.models import Event

def isolate_test():
    db = SessionLocal()
    try:
        print("Testing User count (Rol 4)...")
        c = db.query(User).filter(User.rol_id == 4).count()
        print(f"Success: {c}")

        print("Testing Course count...")
        c = db.query(Course).count()
        print(f"Success: {c}")

        print("Testing Community count (Activo)...")
        c = db.query(Community).filter(Community.status_community == 'Activo').count()
        print(f"Success: {c}")

        print("Testing Event count...")
        c = db.query(Event).count()
        print(f"Success: {c}")
    except Exception as e:
        print(f"FAILED: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    isolate_test()
