from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from ..config.database import Base
from datetime import datetime
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    user_id = Column(String, unique=True, index=True)  # Unique per user
    language = Column(String(10), default="en")  # Default to English
    theme = Column(String(10), default="light")  # light or dark
    text_size = Column(String(10), default="normal")  # small, normal, large
    personalization_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<UserPreference(user_id={self.user_id}, language='{self.language}', theme='{self.theme}')>"