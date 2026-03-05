from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.auth.router import get_current_user # Importante para el candado
from . import schemas, service

router = APIRouter(prefix="/events", tags=["events"])

@router.get("/", response_model=list[schemas.EventResponse])
def list_events(db: Session = Depends(get_db)):
    return service.list_events(db)

@router.post("/", response_model=schemas.EventResponse)
def create_event(
    event: schemas.EventCreate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user) # Activa el candado en Swagger
):
    return service.create_event(db, event, current_user["user_id"])

@router.post("/upload", tags=["events"])
def upload_event_image(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user) # Activa el candado en Swagger
):
    return service.upload_image(file)
