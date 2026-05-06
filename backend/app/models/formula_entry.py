from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class FormulaEntry(Base):
    __tablename__ = "formula_entries"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    page_number = Column(Integer, nullable=False, default=1)
    formula_index = Column(Integer, nullable=False, default=0)
    latex = Column(Text, nullable=False)
    image_path = Column(String(500), nullable=True)
    confidence = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    document = relationship("Document", backref="formula_entries")
