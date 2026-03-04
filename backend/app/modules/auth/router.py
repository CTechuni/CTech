from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import logging
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.config import get_settings
from app.modules.users import service as user_service, schemas as user_schemas
from . import schemas, service
import uuid

logger = logging.getLogger("ctech_api.auth")

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# ── Token Blacklist (in-memory) ────────────────────────────────────────────────
# TODO: In production, use Redis or persistent storage
# This implementation is for single-instance deployments only
_revoked_tokens: set[str] = set()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create JWT access token with expiration.
    
    Args:
        data: Payload data for token
        expires_delta: Custom expiration time, defaults to config value
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    # include issued-at + unique ID so tokens generated within same second differ
    now = datetime.utcnow()
    to_encode.update({"exp": expire, "iat": now, "jti": str(uuid.uuid4())})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Validate JWT token and return user information.
    Ensures token is the most recent valid token for the user (single session).
    
    Args:
        token: JWT token from Authorization header
        db: Database session
        
    Returns:
        Dictionary with user info (email, role, user_id)
        
    Raises:
        HTTPException: If token is invalid, expired, or revoked
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Check if token is revoked
    if token in _revoked_tokens:
        logger.warning(f"Attempt to use revoked token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesión inválida. Por favor vuelve a iniciar sesión.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        email: str | None = payload.get("sub")
        role: str | None = payload.get("role")
        user_id: int | None = payload.get("user_id")
        
        if email is None:
            logger.warning(f"Token missing 'sub' claim")
            raise credentials_exception
        
        # ✅ SINGLE SESSION: Validate token is the most recent for this user
        user = db.query(user_service.models.User).filter(
            user_service.models.User.id == user_id
        ).first()
        
        if not user:
            logger.warning(f"Token references non-existent user: {user_id}")
            raise credentials_exception
        
        # Check if this is the latest valid token for the user
        if user.last_valid_token and user.last_valid_token != token:
            logger.warning(
                f"Attempt to use outdated token for user: {email}. "
                f"User has more recent session."
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Tienes una nueva sesión activa en otro dispositivo/navegador. "
                       "Esta sesión ha sido cerrada por seguridad.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        logger.info(f"Token validated for user: {email}")
        
    except JWTError as e:
        logger.warning(f"JWT validation error: {str(e)}")
        raise credentials_exception
    
    return {"email": email, "role": role, "user_id": user_id}


@router.post("/login", response_model=schemas.TokenResponse)
def login(data: schemas.LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token.
    Implements single session: new login invalidates previous tokens for this user.
    
    Args:
        data: LoginRequest with email and password
        db: Database session
        
    Returns:
        TokenResponse with access token and user info
        
    Raises:
        HTTPException: If credentials are invalid
    """
    user = user_service.authenticate_user(db, data.email, data.password)
    if not user:
        logger.warning(f"Failed login attempt for email: {data.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas",
        )
    
    if user.status != "active":
        logger.warning(f"Login attempt for inactive user: {data.email}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )
    
    logger.info(f"Successful login for user: {data.email}")
    
    # determine role name, default to "user" when missing or null
    if user.role and user.role.name_rol:
        role_name = user.role.name_rol.lower()
    else:
        role_name = "user"

    token_payload = {"sub": user.email, "role": role_name, "user_id": user.id}
    token = create_access_token(token_payload)

    # ✅ SINGLE SESSION: Save token as latest valid token for this user
    # This invalidates any previous sessions
    user.last_valid_token = token
    user.last_token_issued_at = datetime.utcnow()
    user.last_login = datetime.utcnow()
    db.add(user)
    db.commit()
    db.refresh(user)
    
    logger.info(f"Token saved as active session for user: {data.email}, role: {role_name}")

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name_user": user.name_user,
            "role": role_name,
        },
    }


@router.post("/logout")
def logout(
    token: str = Depends(oauth2_scheme),
    current_user: dict = Depends(get_current_user),
):
    """
    Logout user by revoking their token.
    
    Args:
        token: JWT token to revoke
        current_user: Current user info
        
    Returns:
        Success message
    """
    _revoked_tokens.add(token)
    logger.info(f"User logged out: {current_user.get('email')}")
    return {"message": "Sesion cerrada exitosamente"}


@router.post("/forgot-password")
def forgot_password(data: schemas.ForgotPasswordRequest, db: Session = Depends(get_db)):
    """
    Request password reset for user.
    
    Returns success message regardless to prevent email enumeration.
    
    Args:
        data: ForgotPasswordRequest with email
        db: Database session
        
    Returns:
        Generic success message
    """
    success = service.forgot_password(db, data.email)
    if success:
        logger.info(f"Password reset requested for: {data.email}")
    
    # Always return success message for security (don't reveal if email exists)
    return {"message": "Si el email existe, se ha enviado un enlace de recuperacion"}


@router.post("/reset-password")
def reset_password(data: schemas.ResetPasswordRequest, db: Session = Depends(get_db)):
    """
    Reset user password using reset token.
    
    Args:
        data: ResetPasswordRequest with token and new password
        db: Database session
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    success = service.reset_password(db, data.token, data.new_password)
    if not success:
        logger.warning(f"Failed password reset with invalid token")
        raise HTTPException(status_code=400, detail="Token invalido o expirado")
    
    logger.info("Password reset successful")
    return {"message": "Contraseña actualizada exitosamente"}
