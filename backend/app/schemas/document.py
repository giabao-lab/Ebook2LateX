from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DocumentCreate(BaseModel):
    user_id: UUID | None = None
    file_name: str
    file_path_url: str
    latex_content: str | None = None


class DocumentRead(DocumentCreate):
    id: UUID
    upload_date: datetime
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
