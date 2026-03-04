from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SessionBase(BaseModel):
    course_id: int
    start_time: datetime
    end_time: datetime
    meeting_link: Optional[str] = None

class SessionCreate(SessionBase):
    mentor_id: int

class SessionResponse(SessionBase):
    id: int
    mentor_id: int
    is_available: bool
    student_id: Optional[int] = None

    class Config:
        from_attributes = True
