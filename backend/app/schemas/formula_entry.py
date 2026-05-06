from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class FormulaEntryCreate(BaseModel):
    document_id: UUID
    raw_image_path: str | None = None
    latex_content: str
    order_index: int = 0


class FormulaEntryRead(FormulaEntryCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
