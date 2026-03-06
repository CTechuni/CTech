from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.auth.router import get_current_user
from . import schemas, service

router = APIRouter(prefix="/users", tags=["Users"])

# Público
# Protegido
@router.get("/", response_model=list[schemas.UserResponse])
def list_users(db: Session = Depends(get_db), current=Depends(get_current_user)):
    return service.get_all(db)

@router.get("/me", response_model=schemas.UserResponse)
def get_me(current=Depends(get_current_user), db: Session = Depends(get_db)):
    return service.get_user(db, current["user_id"])

@router.patch("/{user_id}/promote")
def promote(user_id: int, db: Session = Depends(get_db), current=Depends(get_current_user)):
    return service.change_role(db, user_id, 2) # 2 para Mentor

@router.patch("/{user_id}/demote")
def demote(user_id: int, db: Session = Depends(get_db), current=Depends(get_current_user)):
    return service.change_role(db, user_id, 4) # 4 para User estándar

@router.get("/leaders", response_model=list[schemas.UserResponse])
def get_leaders(db: Session = Depends(get_db)): #, current=Depends(get_current_user)):
    return service.list_leaders(db)
