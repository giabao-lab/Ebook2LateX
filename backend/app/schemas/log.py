from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class LogCreate(BaseModel):
    formula_id: UUID | None = None
    processing_time_ms: int | None = None
    confidence_score: float | None = None
    error_type: str | None = None
    error_message: str | None = None
    environment_info: dict | None = None


class LogRead(LogCreate):
    log_id: UUID
    timestamp: datetime

    class Config:
        from_attributes = True
