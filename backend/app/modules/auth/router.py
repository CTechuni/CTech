from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.core.database import get_db
from app.core.config import get_settings
from app.modules.users import service as user_service, schemas as user_schemas
from . import schemas, service

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(data: dict):
    return jwt.encode(data, settings.JWT_SECRET_KEY, algorithm="HS256")


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        email: str | None = payload.get("sub")
        role: str | None = payload.get("role")
        user_id: int | None = payload.get("user_id")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return {"email": email, "role": role, "user_id": user_id}


@router.post("/login", response_model=schemas.TokenResponse)
def login(data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = user_service.authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas",
        )

    role_name = user.role.name_rol if user.role else None
    token_payload = {"sub": user.email, "role": role_name, "user_id": user.id}
    token = create_access_token(token_payload)

    return {
        "access_token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "name_user": user.name_user,
            "role": role_name,
        },
    }
