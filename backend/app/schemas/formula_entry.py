from datetime import datetime

from pydantic import BaseModel


class FormulaEntryCreate(BaseModel):
    document_id: int
    page_number: int = 1
    formula_index: int = 0
    latex: str
    image_path: str | None = None
    confidence: float | None = None


class FormulaEntryRead(FormulaEntryCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
