from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, time

class EventBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=150)
    description_event: Optional[str] = Field(None, min_length=10)
    date_events: Optional[date] = None
    time_events: Optional[time] = None
    place: str = Field(..., min_length=3)
    url_form: str
    image: str
    capacity: int = Field(..., ge=1, description="La capacidad debe ser al menos 1")
    status: str

    @field_validator('date_events')
    @classmethod
    def validate_date_not_past(cls, v: date | None) -> date | None:
        if v and v < date.today():
            raise ValueError("La fecha del evento no puede ser en el pasado")
        return v


class EventCreate(EventBase):
    created_by: Optional[int] = None

class EventResponse(EventBase):
    id_event: int
    created_by: Optional[int] = None

    class Config:
        from_attributes = True
