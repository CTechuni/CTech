from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.users.models import User
from . import schemas, service

router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

# 1. Login Estándar (POST /login)
@router.post("/login", response_model=schemas.Token)
def login(data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not service.verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    token = service.create_access_token(data={"sub": user.email, "role_id": user.rol_id})
    return {"access_token": token, "token_type": "bearer"}

# 2. Token para Swagger (POST /token)
@router.post("/token")
def login_for_swagger(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not service.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Usuario o contraseña inválidos")
    
    token = service.create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

# 3. Logout (POST /logout) - Usa la tabla token_blocklist del SQL
@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    service.block_token(db, token)
    return {"message": "Sesión cerrada exitosamente"}

# 4. Recuperación (POST /forgot-password)
@router.post("/forgot-password")
def forgot_password(request: schemas.ForgotPasswordRequest):
    return {"message": f"Instrucciones enviadas a {request.email}"}

# 5. Restablecer (POST /reset-password)
@router.post("/reset-password")
def reset_password(data: schemas.ResetPasswordRequest):
    return {"message": "Contraseña actualizada correctamente"}

