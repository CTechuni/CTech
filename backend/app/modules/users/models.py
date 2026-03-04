from sqlalchemy import Column, Integer, String, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from app.core.database import Base


class Role(Base):
    __tablename__ = "roles"

    id_rol = Column(Integer, primary_key=True, index=True)
    name_rol = Column(String(150), unique=True, nullable=False)
    description = Column(Text)

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name_user = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(150), nullable=False)
    rol_id = Column(Integer, ForeignKey("roles.id_rol"))
    community_id = Column(Integer)
    profile_id = Column(Integer)
    registration_date = Column(TIMESTAMP)
    status = Column(String(50), default="active")

    role = relationship("Role", back_populates="users")