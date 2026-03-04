from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.database import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    instructor_id = Column(Integer, ForeignKey("users.id"))
    price = Column(Float, default=0.0)
    duration = Column(String(50))
    image_url = Column(String(500))
    status = Column(String(50), default="active")

    instructor = relationship("User")
