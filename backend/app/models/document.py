import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True)
    file_name = Column(Text, nullable=False)
    file_path_url = Column(Text, nullable=False)
    upload_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    status = Column(String(50), nullable=False, default="Pending")
    latex_content = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    owner = relationship("User", back_populates="documents")
    formulas = relationship("FormulaEntry", back_populates="document", cascade="all, delete-orphan")
