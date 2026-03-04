from pydantic import BaseModel

class AdminMetricsResponse(BaseModel):
    total_users: int
    total_courses: int
    total_communities: int
    total_events: int
    active_sessions: int

    class Config:
        from_attributes = True
