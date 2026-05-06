from datetime import datetime

from pydantic import BaseModel


class DocumentCreate(BaseModel):
    filename: str
    file_path: str


class DocumentRead(DocumentCreate):
    id: int
    status: str
    latex_content: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
