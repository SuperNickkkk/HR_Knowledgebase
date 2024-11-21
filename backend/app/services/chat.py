from typing import Generator, List
import json
from app.core.config import settings
from app.db.session import SessionLocal
from app.models.chat import ChatMessage, MessageType
import redis
import asyncio

class ChatService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD
        )

    async def generate_response(
        self,
        knowledge_base_id: int,
        message: str,
        session_id: str
    ) -> Generator[str, None, None]:
        # 1. 保存用户消息
        db = SessionLocal()
        try:
            chat_message = ChatMessage(
                session_id=session_id,
                message_type=MessageType.USER,
                content=message
            )
            db.add(chat_message)
            db.commit()

            # 2. 获取知识库内容并生成回答
            references = self._get_relevant_knowledge(knowledge_base_id, message)
            
            # 3. 生成回答
            response_content = ""
            for chunk in self._stream_response(message, references):
                response_content += chunk
                yield json.dumps({
                    "type": "content",
                    "text": chunk
                })

            # 4. 保存AI回答
            ai_message = ChatMessage(
                session_id=session_id,
                message_type=MessageType.AI,
                content=response_content,
                references=json.dumps(references)
            )
            db.add(ai_message)
            db.commit()

        finally:
            db.close()

    def _get_relevant_knowledge(self, knowledge_base_id: int, query: str) -> List[dict]:
        # 实现向量检索相关知识
        # 这里需要集成向量数据库，如 Milvus 或 FAISS
        pass

    def _stream_response(self, query: str, references: List[dict]) -> Generator[str, None, None]:
        # 实现流式响应生成
        # 这里需要集成大模型API
        pass

    @staticmethod
    def get_chat_history(session_id: str) -> List[ChatMessage]:
        db = SessionLocal()
        try:
            return db.query(ChatMessage).filter(
                ChatMessage.session_id == session_id
            ).order_by(ChatMessage.created_at.asc()).all()
        finally:
            db.close()

    @staticmethod
    def save_feedback(message_id: int, feedback: str) -> bool:
        db = SessionLocal()
        try:
            message = db.query(ChatMessage).filter(
                ChatMessage.id == message_id
            ).first()
            if message:
                message.feedback = feedback
                db.commit()
                return True
            return False
        finally:
            db.close() 