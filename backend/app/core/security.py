from passlib.context import CryptContext
import logging

logger = logging.getLogger(__name__)

# Contexto bcrypt para hashing seguro de contraseñas
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        Bcrypt hashed password
        
    Raises:
        ValueError: If password is empty or None
    """
    if not password or not isinstance(password, str):
        raise ValueError("Contraseña inválida: debe ser un string no vacío")
    
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a bcrypt hash.
    
    Args:
        plain_password: Plain text password from user input
        hashed_password: Bcrypt hash from database
        
    Returns:
        True if password matches, False otherwise
        
    Raises:
        ValueError: If inputs are invalid
    """
    if not plain_password or not isinstance(plain_password, str):
        raise ValueError("Contraseña inválida: debe ser un string no vacío")
    
    if not hashed_password or not isinstance(hashed_password, str):
        logger.error("Invalid hashed password format in database")
        return False
    
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Error verifying password: {str(e)}")
        return False
