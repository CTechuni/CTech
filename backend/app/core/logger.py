import logging
import logging.handlers
from pathlib import Path
from app.core.config import get_settings

settings = get_settings()

# Create logs directory if it doesn't exist
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# Configure logger
logger = logging.getLogger("ctech_api")
logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

# Prevent duplicate handlers
if not logger.handlers:
    # File handler - rotating file handler for better management
    file_handler = logging.handlers.RotatingFileHandler(
        filename=LOGS_DIR / "app.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO if not settings.DEBUG else logging.DEBUG)
    
    # Formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    
    file_handler.setFormatter(detailed_formatter)
    console_handler.setFormatter(simple_formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def get_logger(name: str = "ctech_api") -> logging.Logger:
    """Get application logger"""
    return logging.getLogger(name)


# Separate loggers for different modules
security_logger = get_logger("ctech_api.security")
db_logger = get_logger("ctech_api.database")
auth_logger = get_logger("ctech_api.auth")
