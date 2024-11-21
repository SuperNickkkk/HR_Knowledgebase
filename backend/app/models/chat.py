from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from app.db.base import Base
from datetime import datetime
import enum

class MessageType(enum.Enum):
    USER = "user"
    AI = "ai"

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), index=True)
    message_type = Column(Enum(MessageType))
    content = Column(Text, nullable=False)
    references = Column(Text)  # JSON格式存储引用
    feedback = Column(String(20))  # positive/negative
    created_at = Column(DateTime, default=datetime.utcnow) 