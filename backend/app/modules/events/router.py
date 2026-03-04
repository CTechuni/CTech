from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.auth.router import get_current_user
from app.core.cloudinary_service import upload_image
from app.core.logger import get_logger
from . import schemas, service
import logging

logger = get_logger("ctech_api.events")

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/upload")
async def upload_event_image(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload image for event (authenticated users only).
    
    Args:
        file: Image file to upload
        current_user: Current authenticated user
        
    Returns:
        JSON with image URL
        
    Raises:
        HTTPException: If upload fails
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    
    try:
        # Validate file type
        allowed_types = {"image/jpeg", "image/png", "image/gif", "image/webp"}
        if file.content_type not in allowed_types:
            logger.warning(f"Invalid file type attempt: {file.content_type}")
            raise HTTPException(status_code=400, detail="Formato de imagen no válido. Usa JPEG, PNG, GIF o WebP")
        
        url = upload_image(file.file, folder="events")
        if not url:
            logger.error(f"Cloudinary upload failed for user: {current_user.get('email')}")
            raise HTTPException(status_code=500, detail="Error al subir la imagen a Cloudinary")
        
        logger.info(f"Image uploaded successfully by {current_user.get('email')}")
        return {"url": url}
        
    except Exception as e:
        logger.error(f"Error uploading image: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al procesar la imagen")


@router.get("/", response_model=list[schemas.EventResponse])
def list_events(db: Session = Depends(get_db)):
    """
    Get all published events.
    
    Args:
        db: Database session
        
    Returns:
        List of EventResponse
    """
    return service.list_events(db)


@router.post("/", response_model=schemas.EventResponse)
def create_event(
    event: schemas.EventCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Create new event (authenticated users only).
    
    Args:
        event: EventCreate schema
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        EventResponse: Created event
        
    Raises:
        HTTPException: If validation fails
    """
    if not current_user.get("user_id"):
        raise HTTPException(status_code=401, detail="Usuario no autenticado")
    
    try:
        # Validate event data
        if event.capacity < 1:
            raise ValueError("La capacidad debe ser mayor a 0")
        
        user_id = current_user.get("user_id")
        new_event = service.create_event(db, event, user_id)
        logger.info(f"Event created by {current_user.get('email')}: {new_event.id_event}")
        return new_event
        
    except ValueError as e:
        logger.warning(f"Event creation validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating event: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al crear el evento")


@router.put("/{event_id}", response_model=schemas.EventResponse)
def update_event(
    event_id: int,
    event_data: schemas.EventBase,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Update event (creator or admin only).
    
    Args:
        event_id: ID of event to update
        event_data: Updated event data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        EventResponse: Updated event
        
    Raises:
        HTTPException: If not authorized or event not found
    """
    try:
        # Get event to verify ownership or admin status
        db_event = service.get_event_by_id(db, event_id)
        if not db_event:
            logger.warning(f"Update attempt on non-existent event: {event_id}")
            raise HTTPException(status_code=404, detail="Evento no encontrado")
        
        # Check authorization
        is_creator = db_event.created_by == current_user.get("user_id")
        is_admin = current_user.get("role") == "admin"
        
        if not (is_creator or is_admin):
            logger.warning(f"Unauthorized update attempt on event {event_id} by {current_user.get('email')}")
            raise HTTPException(status_code=403, detail="No tienes permisos para actualizar este evento")
        
        updated_event = service.update_event(db, event_id, event_data)
        logger.info(f"Event {event_id} updated by {current_user.get('email')}")
        return updated_event
        
    except ValueError as e:
        logger.warning(f"Event update validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating event: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al actualizar el evento")


@router.delete("/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Delete event (creator or admin only).
    
    Args:
        event_id: ID of event to delete
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If not authorized or event not found
    """
    try:
        # Get event to verify ownership or admin status
        db_event = service.get_event_by_id(db, event_id)
        if not db_event:
            logger.warning(f"Delete attempt on non-existent event: {event_id}")
            raise HTTPException(status_code=404, detail="Evento no encontrado")
        
        # Check authorization
        is_creator = db_event.created_by == current_user.get("user_id")
        is_admin = current_user.get("role") == "admin"
        
        if not (is_creator or is_admin):
            logger.warning(f"Unauthorized delete attempt on event {event_id} by {current_user.get('email')}")
            raise HTTPException(status_code=403, detail="No tienes permisos para eliminar este evento")
        
        success = service.delete_event(db, event_id)
        if not success:
            raise HTTPException(status_code=500, detail="Error al eliminar el evento")
        
        logger.info(f"Event {event_id} deleted by {current_user.get('email')}")
        return {"message": "Evento eliminado exitosamente"}
        
    except Exception as e:
        logger.error(f"Error deleting event: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al eliminar el evento")


# Helper function to get event by ID
def get_event_by_id(db: Session, event_id: int):
    """Helper to get event from service"""
    return service.get_event_by_id(db, event_id)

