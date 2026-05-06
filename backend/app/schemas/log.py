from datetime import datetime

from pydantic import BaseModel


class LogCreate(BaseModel):
    level: str = "INFO"
    message: str
    source: str | None = None


class LogRead(LogCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
