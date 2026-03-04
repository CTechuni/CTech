from pydantic import BaseModel
from typing import Optional

class CommunityBase(BaseModel):
    name_community: str
    description_community: Optional[str] = None
    status_community: str
    code: str
    access_code: Optional[str] = None
    logo_url: Optional[str] = None

class CommunityCreate(CommunityBase):
    pass

class CommunityUpdate(BaseModel):
    name_community: Optional[str] = None
    description_community: Optional[str] = None
    status_community: Optional[str] = None
    access_code: Optional[str] = None
    logo_url: Optional[str] = None

class CommunityLeaderCreate(BaseModel):
    community: CommunityCreate
    leader_id: int

class CommunityResponse(CommunityBase):
    id_community: int

    class Config:
        from_attributes = True
