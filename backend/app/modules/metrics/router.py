from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.auth.router import get_current_user
from . import schemas, service

router = APIRouter(prefix="/metrics", tags=["Metrics"])

@router.get("/admin", response_model=schemas.AdminMetricsResponse)
def get_admin_metrics(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos")
    return service.get_admin_metrics(db)
