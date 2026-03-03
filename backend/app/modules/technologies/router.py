from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from . import schemas, service

router = APIRouter(prefix="/technologies", tags=["technologies"])

@router.get("/", response_model=list[schemas.TechnologyResponse])
def list_technologies(db: Session = Depends(get_db)):
    return service.list_technologies(db)

@router.post("/", response_model=schemas.TechnologyResponse)
def create_technology(technology: schemas.TechnologyCreate, db: Session = Depends(get_db)):
    return service.create_technology(db, technology)

@router.delete("/{technology_id}")
def delete_technology(technology_id: int, db: Session = Depends(get_db)):
    deleted = service.delete_technology(db, technology_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tecnologia no encontrada")
    return {"message": "Tecnologia eliminada"}
