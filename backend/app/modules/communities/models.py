from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base

class Community(Base):
    __tablename__ = "communities"

    id_community = Column(Integer, primary_key=True, index=True)
    name_community = Column(String(150), unique=True, nullable=False)
    description_community = Column(Text)
    status_community = Column(String(150), nullable=False)
    code = Column(String(50), nullable=False)
    access_code = Column(String(50))
    logo_url = Column(Text)
