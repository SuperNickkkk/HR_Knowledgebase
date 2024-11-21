from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class KnowledgeBase(Base):
    __tablename__ = "knowledge_bases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    space_name = Column(String(100), unique=True, nullable=False)
    api_url = Column(String(255))
    model = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"

    id = Column(Integer, primary_key=True, index=True)
    knowledge_base_id = Column(Integer, ForeignKey("knowledge_bases.id"))
    content = Column(Text, nullable=False)
    embedding = Column(Text)  # 存储向量化后的文本
    metadata = Column(Text)  # JSON格式的元数据
    created_at = Column(DateTime, default=datetime.utcnow)

    knowledge_base = relationship("KnowledgeBase", back_populates="chunks") 