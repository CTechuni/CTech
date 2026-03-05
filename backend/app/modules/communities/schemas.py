from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommunityBase(BaseModel):
    name_community: str
    description_community: Optional[str] = None
    status_community: str
    code: str
    access_code: Optional[str] = None
    logo_url: Optional[str] = None

class CommunityCreate(CommunityBase):
    pass

class CommunityUpdate(CommunityBase):
    name_community: Optional[str] = None
    description_community: Optional[str] = None
    status_community: Optional[str] = None

class CommunityResponse(CommunityBase):
    id_community: int
    created_at: datetime

    class Config:
        from_attributes = True
        