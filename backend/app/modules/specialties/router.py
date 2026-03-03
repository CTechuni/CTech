from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from . import schemas, service

router = APIRouter(prefix="/specialties", tags=["specialties"])

@router.get("/", response_model=list[schemas.SpecialtyResponse])
def list_specialties(db: Session = Depends(get_db)):
    return service.list_specialties(db)

@router.post("/", response_model=schemas.SpecialtyResponse)
def create_specialty(specialty: schemas.SpecialtyCreate, db: Session = Depends(get_db)):
    return service.create_specialty(db, specialty)

@router.delete("/{specialty_id}")
def delete_specialty(specialty_id: int, db: Session = Depends(get_db)):
    deleted = service.delete_specialty(db, specialty_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Especialidad no encontrada")
    return {"message": "Especialidad eliminada"}
