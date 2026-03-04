from sqlalchemy.orm import Session
from app.modules.users import service as user_service

# Este servicio actua como puente para la logica de autenticacion
def authenticate(db: Session, email: str, password: str):
    return user_service.authenticate_user(db, email, password)
