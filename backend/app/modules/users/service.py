from sqlalchemy.orm import Session
from . import repository, models


def authenticate_user(db: Session, email: str, password: str):
    user = repository.get_user_by_email(db, email)
    if not user:
        return None
    # por ahora comparamos el hash directamente; reemplazar con algo seguro en produccion
    if user.password_hash != password:
        return None
    return user
