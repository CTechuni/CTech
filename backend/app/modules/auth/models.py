from sqlalchemy import Column, Integer, Text, DateTime, func
from app.core.database import Base

# NOTA: No definas Role aquí. 
# SQLAlchemy ya lo cargó desde app/modules/users/models.py

class TokenBlocklist(Base):
    __tablename__ = "token_blocklist"
    __table_args__ = {'extend_existing': True} # Para evitar errores al recargar el servidor
    
    id = Column(Integer, primary_key=True, index=True)
    token = Column(Text, nullable=False, index=True)
    blacklisted_at = Column(DateTime, server_default=func.now())