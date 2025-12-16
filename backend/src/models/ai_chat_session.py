from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..config.database import Base
from datetime import datetime
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class AIChatSession(Base):
    __tablename__ = "ai_chat_sessions"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    user_id = Column(String, index=True)  # Optional, for authenticated users
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)

    # Relationship to chat messages
    messages = relationship("AIChatMessage", back_populates="session", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<AIChatSession(id={self.id}, user_id='{self.user_id}', is_active={self.is_active})>"


class AIChatMessage(Base):
    __tablename__ = "ai_chat_messages"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    session_id = Column(String, ForeignKey("ai_chat_sessions.id"), nullable=False)
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    context_used = Column(Text)  # The textbook content used as context for the response

    # Relationship to the session
    session = relationship("AIChatSession", back_populates="messages")

    def __repr__(self):
        return f"<AIChatMessage(id={self.id}, session_id={self.session_id}, role='{self.role}')>"