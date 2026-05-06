import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class FormulaEntry(Base):
    __tablename__ = "formula_entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    raw_image_path = Column(Text, nullable=True)
    latex_content = Column(Text, nullable=False)
    order_index = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    document = relationship("Document", back_populates="formula_entries")
    logs = relationship("Log", back_populates="formula_entry", cascade="all, delete-orphan")
