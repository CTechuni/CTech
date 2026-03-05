from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.auth.router import get_current_user
from . import schemas, service

router = APIRouter(prefix="/communities", tags=["Communities"])

# Listado público
@router.get("/", response_model=list[schemas.CommunityResponse])
def get_communities(db: Session = Depends(get_db)):
    return service.list_communities(db)

# Creación protegida
@router.post("/", response_model=schemas.CommunityResponse)
def create_community(data: schemas.CommunityCreate, db: Session = Depends(get_db), current=Depends(get_current_user)):
    return service.create_community(db, data)

# Actualización protegida
@router.patch("/{id}", response_model=schemas.CommunityResponse)
def update_community(id: int, data: schemas.CommunityUpdate, db: Session = Depends(get_db), current=Depends(get_current_user)):
    return service.update_community(db, id, data)

# Eliminación protegida
@router.delete("/{id}")
def delete_community(id: int, db: Session = Depends(get_db), current=Depends(get_current_user)):
    return service.delete_community(db, id)