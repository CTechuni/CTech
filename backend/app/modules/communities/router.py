from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from . import schemas, service
from fastapi import File, UploadFile
from app.modules.auth.router import get_current_user
from app.core.cloudinary_service import upload_image

router = APIRouter(prefix="/communities", tags=["communities"])

@router.post("/upload")
async def upload_community_logo(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos")
    url = upload_image(file.file, folder="communities")
    if not url:
        raise HTTPException(status_code=500, detail="Error al subir la imagen a Cloudinary")
    return {"url": url}

@router.get("/", response_model=list[schemas.CommunityResponse])
def list_communities(db: Session = Depends(get_db)):
    return service.list_communities(db)

@router.post("/", response_model=schemas.CommunityResponse)
def create_community(community: schemas.CommunityCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos")
    return service.create_community(db, community)

@router.post("/with-leader", response_model=schemas.CommunityResponse)
def create_community_with_leader(data: schemas.CommunityLeaderCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos")
    return service.create_community_with_leader(db, data)

@router.post("/{id}/assign-user/{user_id}")
def assign_user(id: int, user_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Solo admin o el lider de esa comunidad (si implementamos esa logica luego)
    if current_user["role"] not in ["admin", "leader"]:
        raise HTTPException(status_code=403, detail="No tienes permisos")
    service.assign_user(db, id, user_id)
    return {"message": "Usuario asignado exitosamente"}

@router.patch("/{id}", response_model=schemas.CommunityResponse)
def update_community(id: int, updates: schemas.CommunityUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos")
    return service.update_community(db, id, updates)

@router.delete("/{id}")
def delete_community(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos")
    service.delete_community(db, id)
    return {"message": "Comunidad eliminada"}

