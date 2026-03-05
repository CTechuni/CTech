from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Timestamp, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    name_user = Column(String(150))
    rol_id = Column(Integer, ForeignKey("roles.id_rol"))
    status = Column(String(50), default="active")
    is_email_verified = Column(Boolean, default=False)
    created_at = Column(Timestamp, server_default=func.now())

    role = relationship("Role")
