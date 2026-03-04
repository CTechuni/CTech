from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from . import schemas, service

router = APIRouter(prefix="/communities", tags=["communities"])

@router.get("/", response_model=list[schemas.CommunityResponse])
def list_communities(db: Session = Depends(get_db)):
    return service.list_communities(db)

@router.post("/", response_model=schemas.CommunityResponse)
def create_community(community: schemas.CommunityCreate, db: Session = Depends(get_db)):
    return service.create_community(db, community)
