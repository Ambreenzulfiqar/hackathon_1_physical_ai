from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from ..config.database import Base
from datetime import datetime
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class TextbookChapter(Base):
    __tablename__ = "textbook_chapters"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False, index=True)
    content = Column(Text, nullable=False)
    order = Column(Integer, nullable=False)
    word_count = Column(Integer, default=0)
    estimated_reading_time = Column(Integer, default=0)  # in minutes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<TextbookChapter(id={self.id}, title='{self.title}', order={self.order})>"