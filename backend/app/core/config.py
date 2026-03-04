from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database configuration (required)
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    
    # JWT Configuration (required)
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Cloudinary Configuration (required)
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    # Admin Configuration (required - must be set in environment)
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str
    
    # Environment
    ENVIRONMENT: str = "production"  # "development", "staging", "production"
    DEBUG: bool = False
    
    # CORS Configuration
    ALLOWED_ORIGINS: str = "http://localhost:4321"  # Comma-separated list

    @property
    def DATABASE_URL(self):
        # Strip potential quotes from environment variables
        user = self.DB_USER.strip('"') if self.DB_USER else ""
        password = self.DB_PASSWORD.strip('"') if self.DB_PASSWORD else ""
        host = self.DB_HOST.strip('"') if self.DB_HOST else "localhost"
        port = self.DB_PORT.strip('"') if self.DB_PORT else "5432"
        db_name = self.DB_NAME.strip('"') if self.DB_NAME else ""

        url = (
            f"postgresql+psycopg://{user}:{password}@"
            f"{host}:{port}/{db_name}"
        )
        return url
    
    @property
    def get_allowed_origins(self) -> list[str]:
        """Parse comma-separated allowed origins"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        extra = "ignore"  # Allow extra environment variables during tests/deployment


# Global settings instance (cached)
_settings: Optional[Settings] = None

def get_settings() -> Settings:
    """Get or create settings singleton"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
