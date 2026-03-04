from sqlalchemy import Column, Integer, String, Text, Date, Time, ForeignKey
from app.core.database import Base

class Event(Base):
    __tablename__ = "events"

    id_event = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description_event = Column(Text)
    date_events = Column(Date)
    time_events = Column(Time)
    place = Column(String(155), nullable=False)
    url_form = Column(String(255), nullable=False)
    image = Column(String(255), nullable=False)
    capacity = Column(Integer, nullable=False, default=0)
    created_by = Column(Integer, ForeignKey("users.id"))
    status = Column(String(50), nullable=False, default="active")

