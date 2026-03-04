from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.auth.router import get_current_user
from . import schemas, service

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("/", response_model=list[schemas.CourseResponse])
def list_courses(db: Session = Depends(get_db)):
    return service.list_courses(db)

@router.get("/{id}", response_model=schemas.CourseResponse)
def get_course(id: int, db: Session = Depends(get_db)):
    db_obj = service.get_course(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return db_obj

@router.post("/", response_model=schemas.CourseResponse)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos")
    return service.create_course(db, course)

@router.put("/{id}", response_model=schemas.CourseResponse)
def update_course(id: int, updates: schemas.CourseUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos")
    db_obj = service.update_course(db, id, updates)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return db_obj

@router.delete("/{id}")
def delete_course(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos")
    service.delete_course(db, id)
    return {"message": "Curso eliminado"}
