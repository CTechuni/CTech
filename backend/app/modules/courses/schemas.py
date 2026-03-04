from pydantic import BaseModel, Field
from typing import Optional

class CourseBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=150)
    description: Optional[str] = Field(None, min_length=10)
    price: float = Field(default=0.0, ge=0.0, description="El precio no puede ser negativo")
    duration: Optional[str] = None
    image_url: Optional[str] = None
    status: str = "active"

class CourseCreate(CourseBase):
    instructor_id: int

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    duration: Optional[str] = None
    image_url: Optional[str] = None
    status: Optional[str] = None

class CourseResponse(CourseBase):
    id: int
    instructor_id: int

    class Config:
        from_attributes = True
