from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
from app.core.config import get_settings
from app.core.logger import get_logger

logger = get_logger(__name__)

settings = get_settings()

# Connection pooling disabled for Vercel/serverless compatibility
# In production with traditional servers, consider using QueuePool
pool_class = NullPool if settings.ENVIRONMENT == "production" else None

try:
    # if running under pytest, allow overriding to an in-memory SQLite URL
    db_url = getattr(settings, "DATABASE_URL", None)
    # the tests may set settings.DATABASE_URL to 'sqlite:///:memory:'
    engine = create_engine(
        db_url,
        poolclass=pool_class,
        echo=settings.DEBUG,  # Log SQL queries only in debug mode
        connect_args={"connect_timeout": 10} if db_url and db_url.startswith("postgres") else {}
    )
    logger.info(f"Database engine created for {settings.ENVIRONMENT} environment")
except Exception as e:
    logger.error(f"Failed to create database engine: {str(e)}")
    raise

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

Base = declarative_base()


def get_db():
    """
    Dependency for obtaining database session.
    Automatically handles rollback on error.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    """Initialize database schema"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise
