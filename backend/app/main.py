from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importación de Routers
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
from app.modules.communities.router import router as communities_router
from app.modules.content.router import router as content_router
from app.modules.courses.router import router as courses_router
from app.modules.events.router import router as events_router
from app.modules.mentoring_sessions.router import router as mentoring_router
from app.modules.metrics.router import router as metrics_router
from app.modules.specialties.router import router as specialties_router
from app.modules.technologies.router import router as technologies_router
from app.modules.admin.router import router as admin_router

app = FastAPI(
    title="CTech API",
    description="Plataforma LMS para comunidades tecnológicas en Colombia",
    version="1.0.0"
)

# Configuración de CORS (Vital para que el Frontend se conecte)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción cambia esto por tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de Rutas con prefijo de versión v1
api_prefix = "/api/v1"

app.include_router(auth_router, prefix=api_prefix)
app.include_router(users_router, prefix=api_prefix)
app.include_router(communities_router, prefix=api_prefix)
app.include_router(content_router, prefix=api_prefix)
app.include_router(courses_router, prefix=api_prefix)
app.include_router(events_router, prefix=api_prefix)
app.include_router(mentoring_router, prefix=api_prefix)
app.include_router(metrics_router, prefix=api_prefix)
app.include_router(specialties_router, prefix=api_prefix)
app.include_router(technologies_router, prefix=api_prefix)
app.include_router(admin_router, prefix=api_prefix)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenido a CTech API - Proyecto SENA Ficha 2995403"}