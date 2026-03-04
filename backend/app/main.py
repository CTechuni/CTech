from fastapi import FastAPI
from app.modules.content.router import router as content_router
from app.modules.communities.router import router as communities_router
from app.modules.events.router import router as events_router
from app.modules.auth.router import router as auth_router
from app.modules.admin.router import router as admin_router
from app.modules.technologies.router import router as technologies_router
from app.modules.specialties.router import router as specialties_router
from app.core.database import engine, Base, SessionLocal
from app.modules.users.models import Role, User

# Create tables
Base.metadata.create_all(bind=engine)

# Seed basic data
db = SessionLocal()
try:
    if not db.query(Role).first():
        roles = [Role(name="admin"), Role(name="mentor"), Role(name="leader"), Role(name="user")]
        db.add_all(roles)
        db.commit()
    
    admin_role = db.query(Role).filter_by(name="admin").first()
    if not db.query(User).filter_by(email="admin@example.com").first():
        admin_user = User(
            full_name="Admin Principal",
            email="admin@example.com",
            hashed_password="admin", # In production use hashing!
            role_id=admin_role.id_role
        )
        db.add(admin_user)
        db.commit()
finally:
    db.close()

app = FastAPI()

app.include_router(content_router)
app.include_router(communities_router)
app.include_router(events_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(technologies_router)
app.include_router(specialties_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
