from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

# El nombre 'router' es lo que el main.py está buscando importar
router = APIRouter()

@router.post("/", tags=["Mentoring Sessions"])
def create_session(db: Session = Depends(get_db)):
    return {"message": "Sesión creada"}

@router.get("/course/{course_id}", tags=["Mentoring Sessions"])
def get_sessions(course_id: int, db: Session = Depends(get_db)):
    return []

@router.post("/{id}/reserve", tags=["Mentoring Sessions"])
def reserve_session(id: int, db: Session = Depends(get_db)):
    return {"message": "Reserva exitosa"}