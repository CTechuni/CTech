from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class ThematicArea(Base):
    __tablename__ = "thematic_areas"
    id_area = Column(Integer, primary_key=True, index=True)
    name_area = Column(String(150), unique=True, nullable=False)
    description_area = Column(Text, nullable=True)

class LearningLevel(Base):
    __tablename__ = "learning_levels"
    id_level = Column(Integer, primary_key=True, index=True)
    name_level = Column(String(150), unique=True, nullable=False)
    description_level = Column(Text, nullable=True)

class EducationalContent(Base):
    __tablename__ = "educational_content"

    id_content = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description_content = Column(Text, nullable=True)
    url_file = Column(String(150), nullable=True)
    type_content = Column(String(150), nullable=False)
    area_id = Column(Integer, ForeignKey("thematic_areas.id_area"), nullable=False)
    level_id = Column(Integer, ForeignKey("learning_levels.id_level"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    upload_date = Column(DateTime, server_default=func.now())
    status_content = Column(String(50), nullable=False, default="activo")

    area = relationship("ThematicArea")
    level = relationship("LearningLevel")
    author = relationship("User")

