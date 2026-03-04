from sqlalchemy import Column, Integer, String, ForeignKey, Text, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class Role(Base):
    __tablename__ = "roles"

    id_rol = Column(Integer, primary_key=True, index=True)
    name_rol = Column(String(150), unique=True, nullable=False)
    description = Column(Text)

    users = relationship("User", back_populates="role")


class Profile(Base):
    __tablename__ = "profiles"

    id_profile = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255))
    email = Column(String(255), unique=True)
    photo_url = Column(Text)
    specialization = Column(String(255))
    status = Column(String(50))
    registration_date = Column(TIMESTAMP)
    last_login = Column(TIMESTAMP)
    community_id = Column(Integer)
    rol_id = Column(Integer)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name_user = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    rol_id = Column(Integer, ForeignKey("roles.id_rol"))
    community_id = Column(Integer, ForeignKey("communities.id_community"), nullable=True)
    specialty_id = Column(Integer, ForeignKey("specialties.id"), nullable=True)
    profile_id = Column(Integer, ForeignKey("profiles.id_profile"), nullable=True)

    registration_date = Column(TIMESTAMP, default=datetime.utcnow)
    last_login = Column(TIMESTAMP, nullable=True)
    status = Column(String(50), default="active", index=True)
    is_email_verified = Column(Boolean, default=False)

    # Session management for preventing multiple active sessions
    last_valid_token = Column(String(500), nullable=True)
    last_token_issued_at = Column(TIMESTAMP, nullable=True)

    role = relationship("Role", back_populates="users")
    profile = relationship("Profile")