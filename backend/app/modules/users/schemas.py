from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    name_user: str = Field(..., min_length=2, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    rol_id: int | None = None
    community_id: int | None = None
    invite_code: str | None = None  # debe coincidir con el código de la comunidad seleccionada

class UserUpdate(BaseModel):
    name_user: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None = None
    status: str | None = None
    photo_url: str | None = None

class UserOut(UserBase):
    id: int
    role: str | None = None
    status: str
    registration_date: str | None = None
    photo_url: str | None = None

    class Config:
        from_attributes = True

class PromoteMentorRequest(BaseModel):
    specialty_id: int

