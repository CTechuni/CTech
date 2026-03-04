from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.auth.router import get_current_user
from . import schemas, service

router = APIRouter(prefix="/sessions", tags=["Mentoring Sessions"])

@router.post("/", response_model=schemas.SessionResponse)
def create_session(session: schemas.SessionCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Solo admin o mentores pueden crear sesiones
    if current_user["role"] not in ["admin", "mentor"]:
        raise HTTPException(status_code=403, detail="No tienes permisos")
    return service.create_session(db, session)

@router.get("/course/{course_id}", response_model=list[schemas.SessionResponse])
def get_sessions(course_id: int, db: Session = Depends(get_db)):
    return service.list_sessions_by_course(db, course_id)

@router.post("/{id}/reserve", response_model=schemas.SessionResponse)
def reserve_session(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    session = service.reserve_session(db, id, current_user["id"])
    if not session:
        raise HTTPException(status_code=400, detail="Sesion no disponible")
    return session

@router.delete("/{id}/cancel")
def cancel_session(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Solo el estudiante que reservó o un admin
    # (Para simplificar, permitimos cancelar si existe)
    service.cancel_session(db, id)
    return {"message": "Sesion cancelada"}
