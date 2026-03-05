from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from . import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "CTECH_SECRET_KEY_2026" # Cambiar por una segura
ALGORITHM = "HS256"

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def block_token(db: Session, token: str):
    """Registra el token en la tabla de bloqueo según el SQL"""
    db_token = models.TokenBlocklist(token=token, blacklisted_at=datetime.utcnow())
    db.add(db_token)
    db.commit()
