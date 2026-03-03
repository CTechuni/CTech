from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from . import schemas, service

router = APIRouter(prefix="/events", tags=["events"])

@router.get("/", response_model=list[schemas.EventResponse])
def list_events(db: Session = Depends(get_db)):
    return service.list_events(db)

@router.post("/", response_model=schemas.EventResponse)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return service.create_event(db, event)
