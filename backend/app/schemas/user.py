from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: str | None = None
    role: str = "Editor"


class UserRead(BaseModel):
    user_id: UUID
    username: str
    email: str
    full_name: str | None = None
    role: str
    last_login: datetime | None = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
