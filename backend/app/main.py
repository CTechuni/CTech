from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

# Database and Models
from app.core.database import engine, SessionLocal, init_db
from app.core.config import get_settings
from app.db.base_api import Base  # This imports all models automatically
from app.db.init_db import seed_data

# Routers
from app.modules.users.router import router as users_router
from app.modules.courses.router import router as courses_router
from app.modules.mentoring_sessions.router import router as sessions_router
from app.modules.metrics.router import router as metrics_router
from app.modules.content.router import router as content_router
from app.modules.communities.router import router as communities_router
from app.modules.events.router import router as events_router
from app.modules.auth.router import router as auth_router
from app.modules.admin.router import router as admin_router
from app.modules.technologies.router import router as technologies_router
from app.modules.specialties.router import router as specialties_router

settings = get_settings()
logger = logging.getLogger("ctech_api")

# ── Database Initialization (one-time only) ───────────────────────────────────
init_db()

# Seed data only once - check if data exists before seeding
def init_seed_data():
    """Initialize seed data only if database is empty"""
    db = SessionLocal()
    try:
        from app.modules.users.models import Role
        # Only seed if no roles exist
        if db.query(Role).count() == 0:
            logger.info("Database is empty, seeding initial data...")
            seed_data(db)
        else:
            logger.info("Database already contains data, skipping seed")
    except Exception as e:
        logger.error(f"Error during seed initialization: {str(e)}")
    finally:
        db.close()

# ── App Configuration ────────────────────────────────────────────────────────
app = FastAPI(
    title="CTech API",
    description="Backend para la plataforma CTech",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,  # Disable docs in production
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
)

# ── CORS Middleware (Restrictive configuration) ───────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Explicit methods only
    allow_headers=["Content-Type", "Authorization"],  # Explicit headers only
    max_age=600,  # Cache CORS headers for 10 minutes
)

# ── Global Exception Handler ─────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler to catch unhandled errors"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    # In production, don't expose internal details
    if settings.ENVIRONMENT == "production":
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )
    else:
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc)}
        )

# ── Health Check ─────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
def health_check():
    """Endpoint to check API health status"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": "1.0.0"
    }

@app.get("/", tags=["Root"])
def read_root():
    """Root endpoint"""
    return {
        "message": "Welcome to CTech API",
        "docs": "/docs" if settings.DEBUG else "Documentation disabled in production"
    }

# ── Routing ──────────────────────────────────────────────────────────────────
api_router = APIRouter(prefix="/api/v1")

# Include all routers
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(communities_router)
api_router.include_router(courses_router)
api_router.include_router(sessions_router)
api_router.include_router(metrics_router)
api_router.include_router(events_router)
api_router.include_router(content_router)
api_router.include_router(technologies_router)
api_router.include_router(specialties_router)
api_router.include_router(admin_router)

app.include_router(api_router)

# ── Startup Event ────────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    """Initialize seed data on startup"""
    logger.info(f"Application starting up in {settings.ENVIRONMENT} mode")
    init_seed_data()

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Application shutting down")

