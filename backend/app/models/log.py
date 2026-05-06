import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class Log(Base):
    __tablename__ = "logs"

    log_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    formula_id = Column(UUID(as_uuid=True), ForeignKey("formula_entries.id", ondelete="CASCADE"), nullable=True)
    processing_time_ms = Column(Integer, nullable=True)
    confidence_score = Column(Numeric(3, 2), nullable=True)
    error_type = Column(String(100), nullable=True)
    error_message = Column(Text, nullable=True)
    environment_info = Column(JSONB, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    formula_entry = relationship("FormulaEntry", back_populates="logs")
