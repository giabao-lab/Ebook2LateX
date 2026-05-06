from sqlalchemy import Column, DateTime, Integer, String, Text, func

from app.core.database import Base


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(20), nullable=False, default="INFO")
    message = Column(Text, nullable=False)
    source = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
