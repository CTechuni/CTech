from fastapi import FastAPI
from app.modules.content.router import router as contenido_router
from app.modules.auth.router import router as auth_router
from app.modules.admin.router import router as admin_router
from app.modules.specialties.router import router as specialties_router
from app.modules.technologies.router import router as technologies_router
from app.modules.events.router import router as events_router
from app.modules.communities.router import router as communities_router

app = FastAPI(title="CTech API")

# crear tablas automaticamente en el motor configurado (util para desarrollo)
from app.core.database import engine, Base, SessionLocal
from app.modules.users import models as user_models

Base.metadata.create_all(bind=engine)

# inicializar datos basicos (roles, cuenta admin) si no existen
def _initialize_seed_data():
    db = SessionLocal()
    try:
        # asegurar roles basicos
        for role_name in ("user", "mentor", "leader", "admin"):
            if not db.query(user_models.Role).filter_by(name_rol=role_name).first():
                db.add(user_models.Role(name_rol=role_name))
        db.commit()

        # crear usuario administrador de prueba
        if not db.query(user_models.User).filter_by(email="admin@example.com").first():
            admin_role = db.query(user_models.Role).filter_by(name_rol="admin").first()
            db.add(user_models.User(
                name_user="Administrador",
                email="admin@example.com",
                password_hash="admin",
                rol_id=admin_role.id_rol
            ))
            db.commit()
    finally:
        db.close()

_initialize_seed_data()

app.include_router(contenido_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(specialties_router)
app.include_router(technologies_router)
app.include_router(events_router)
app.include_router(communities_router)

@app.get("/")
def read_root():
    return {"message": "Hola desde API de CTech funcionando"}
