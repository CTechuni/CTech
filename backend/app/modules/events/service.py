from sqlalchemy.orm import Session
from fastapi import UploadFile
from . import repository, schemas

def list_events(db: Session):
    return repository.get_all_events(db)

def create_event(db: Session, event: schemas.EventCreate, user_id: int):
    return repository.create_event(db, event, user_id)

def upload_image(file: UploadFile):
    # Lógica para procesar la imagen (Cloudinary)
    # Por ahora devolvemos la info para el Swagger
    return {
        "filename": file.filename,
        "message": "Upload Event Image: Exitosa",
        "url": f"https://res.cloudinary.com/ctech/image/upload/{file.filename}"
    }
