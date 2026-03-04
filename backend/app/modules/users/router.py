from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.auth.router import get_current_user
from app.core.logger import get_logger
from . import service, schemas
import logging

logger = get_logger("ctech_api.users")

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    
    Args:
        user: UserCreate schema with email and password
        db: Database session
        
    Returns:
        UserOut: Created user information
        
    Raises:
        HTTPException: If email already exists or validation fails
    """
    try:
        # Check if email already exists
        existing_user = service.get_user_by_email(db, email=user.email)
        if existing_user:
            logger.warning(f"Registration attempt with existing email: {user.email}")
            raise HTTPException(status_code=400, detail="Email ya registrado")
        
        # Create new user
        new_user = service.create_user(db=db, user_data=user.dict())
        logger.info(f"New user registered: {user.email}")
        return new_user
        
    except ValueError as e:
        logger.error(f"Validation error during registration: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error during user registration: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al crear el usuario")


@router.get("/", response_model=list[schemas.UserOut])
def list_users(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    List all users (admin only).
    
    Args:
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List of UserOut
        
    Raises:
        HTTPException: If user is not admin
    """
    if current_user["role"] != "admin":
        logger.warning(f"Unauthorized access to user list by: {current_user.get('email')}")
        raise HTTPException(status_code=403, detail="No tienes permisos")
    
    return service.get_all_users(db)


@router.get("/me", response_model=schemas.UserOut)
def get_me(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get current user profile.
    
    Args:
        current_user: Authenticated user
        db: Database session
        
    Returns:
        UserOut: Current user information
    """
    user = service.get_user(db, current_user["user_id"])
    if not user:
        logger.error(f"User not found: {current_user['user_id']}")
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.patch("/me", response_model=schemas.UserOut)
def update_profile(
    updates: schemas.UserUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user profile.
    
    Args:
        updates: UserUpdate schema
        current_user: Authenticated user
        db: Database session
        
    Returns:
        UserOut: Updated user information
    """
    try:
        user = service.update_user(db, current_user["user_id"], updates.dict(exclude_unset=True))
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        logger.info(f"User updated: {current_user['email']}")
        return user
    except Exception as e:
        logger.error(f"Error updating user profile: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al actualizar el perfil")


@router.get("/leaders", response_model=list[schemas.UserOut])
def list_leaders(db: Session = Depends(get_db)):
    """Get all users with leader role"""
    users = service.get_users_by_role(db, "leader")
    return users


@router.get("/mentors", response_model=list[schemas.UserOut])
def list_mentors(db: Session = Depends(get_db)):
    """Get all users with mentor role"""
    users = service.get_users_by_role(db, "mentor")
    return users


@router.patch("/{user_id}/promote", response_model=schemas.UserOut)
def promote_user(
    user_id: int,
    request: schemas.PromoteMentorRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Promote user to mentor (admin only).
    
    Args:
        user_id: ID of user to promote
        request: PromoteMentorRequest with specialty_id
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        UserOut: Updated user
        
    Raises:
        HTTPException: If user is not admin or target user not found
    """
    if current_user["role"] != "admin":
        logger.warning(f"Unauthorized promotion attempt by: {current_user.get('email')}")
        raise HTTPException(status_code=403, detail="No tienes permisos")
    
    user = service.promote_to_mentor(db, user_id, request.specialty_id)
    if not user:
        logger.warning(f"Promotion failed - user not found: {user_id}")
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    logger.info(f"User {user_id} promoted to mentor by {current_user.get('email')}")
    return user


@router.patch("/{user_id}/demote", response_model=schemas.UserOut)
def demote_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Demote user from mentor to regular user (admin only).
    
    Args:
        user_id: ID of user to demote
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        UserOut: Updated user
        
    Raises:
        HTTPException: If user is not admin or target user not found
    """
    if current_user["role"] != "admin":
        logger.warning(f"Unauthorized demotion attempt by: {current_user.get('email')}")
        raise HTTPException(status_code=403, detail="No tienes permisos")
    
    user = service.demote_to_user(db, user_id)
    if not user:
        logger.warning(f"Demotion failed - user not found: {user_id}")
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    logger.info(f"User {user_id} demoted to user by {current_user.get('email')}")
    return user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Delete user (admin only, no self-deletion).
    
    Args:
        user_id: ID of user to delete
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If user is not admin, user not found, or trying to delete self
    """
    if current_user["role"] != "admin":
        logger.warning(f"Unauthorized deletion attempt by: {current_user.get('email')}")
        raise HTTPException(status_code=403, detail="No tienes permisos")
    
    # Prevent self-deletion
    if user_id == current_user["user_id"]:
        logger.warning(f"Admin attempted self-deletion: {current_user.get('email')}")
        raise HTTPException(status_code=400, detail="No puedes eliminar tu propia cuenta")
    
    success = service.delete_user(db, user_id)
    if not success:
        logger.warning(f"Deletion failed - user not found: {user_id}")
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    logger.info(f"User {user_id} deleted by {current_user.get('email')}")
    return {"message": "Usuario eliminado exitosamente"}
