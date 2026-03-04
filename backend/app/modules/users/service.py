from sqlalchemy.orm import Session
from . import repository, models
from app.core import security
from app.core.logger import get_logger
from app.modules.communities.models import Community as CommunityModel
import logging

logger = get_logger("ctech_api.users")


def authenticate_user(db: Session, email: str, password: str):
    """
    Authenticate user with email and password.
    
    Args:
        db: Database session
        email: User email
        password: Plain text password
        
    Returns:
        User object if credentials are valid, None otherwise
    """
    user = repository.get_user_by_email(db, email)
    if not user:
        logger.warning(f"Authentication attempt for non-existent email: {email}")
        return None
    
    try:
        if not security.verify_password(password, user.password_hash):
            logger.warning(f"Authentication failed for user: {email}")
            return None
    except ValueError as e:
        logger.error(f"Error verifying password for user {email}: {str(e)}")
        return None
    
    return user


def get_user_by_email(db: Session, email: str):
    """Get user by email"""
    return repository.get_user_by_email(db, email)


def create_user(db: Session, user_data: dict):
    """
    Create new user with hashed password.
    
    Args:
        db: Database session
        user_data: Dictionary with user information
        
    Returns:
        Created User object
        
    Raises:
        ValueError: If required fields are missing or invalid
    """
    if "password" not in user_data:
        raise ValueError("La contraseña es requerida")
    
    # Hash password before saving
    try:
        user_data["password_hash"] = security.get_password_hash(user_data.pop("password"))
    except ValueError as e:
        logger.error(f"Error hashing password: {str(e)}")
        raise
    
    # Verify community/inviteCode if provided
    if "community_id" in user_data and user_data["community_id"] is not None:
        cid = user_data["community_id"]
        community = db.query(CommunityModel).filter(CommunityModel.id_community == cid).first()
        if not community:
            raise ValueError("Comunidad inválida")
        # check invite code if given
        invite = user_data.pop("invite_code", None)
        if invite is not None and invite != community.access_code:
            raise ValueError("Código de invitación incorrecto para la comunidad seleccionada")
    else:
        # if community_id not supplied but invite_code is present, ignore it
        if "invite_code" in user_data:
            user_data.pop("invite_code")

    # Default role if not provided
    if "rol_id" not in user_data or user_data["rol_id"] is None:
        role = repository.get_role_by_name(db, "user")
        if not role:
            raise ValueError("Role 'user' not found in database")
        user_data["rol_id"] = role.id_rol
    
    # Ensure user status is active by default
    if "status" not in user_data:
        user_data["status"] = "active"
    
    logger.info(f"Creating new user with email: {user_data.get('email')}")
    return repository.create_user(db, user_data)


def get_users_by_role(db: Session, role_name: str):
    """Get all users with a specific role"""
    return repository.get_users_by_role(db, role_name)


def get_all_users(db: Session):
    """Get all users"""
    return repository.get_all_users(db)


def get_user(db: Session, user_id: int):
    """Get user by ID"""
    user = repository.get_user_by_id(db, user_id)
    if not user:
        logger.warning(f"User not found: {user_id}")
    return user


def promote_to_mentor(db: Session, user_id: int, specialty_id: int):
    """
    Promote user to mentor role.
    
    Args:
        db: Database session
        user_id: ID of user to promote
        specialty_id: Specialty ID for mentor
        
    Returns:
        Updated User object or None if user not found
    """
    role = repository.get_role_by_name(db, "mentor")
    if not role:
        logger.error("Mentor role not found in database")
        return None
    
    logger.info(f"Promoting user {user_id} to mentor with specialty {specialty_id}")
    return repository.update_user(db, user_id, {
        "rol_id": role.id_rol,
        "specialty_id": specialty_id
    })


def demote_to_user(db: Session, user_id: int):
    """
    Demote user to regular user role.
    
    Args:
        db: Database session
        user_id: ID of user to demote
        
    Returns:
        Updated User object or None if user not found
    """
    role = repository.get_role_by_name(db, "user")
    if not role:
        logger.error("User role not found in database")
        return None
    
    logger.info(f"Demoting user {user_id} to user role")
    return repository.update_user(db, user_id, {"rol_id": role.id_rol})


def update_user(db: Session, user_id: int, updates: dict):
    """Update user information"""
    logger.info(f"Updating user {user_id}")
    return repository.update_user(db, user_id, updates)


def delete_user(db: Session, user_id: int):
    """Delete user"""
    logger.info(f"Deleting user {user_id}")
    return repository.delete_user(db, user_id)
