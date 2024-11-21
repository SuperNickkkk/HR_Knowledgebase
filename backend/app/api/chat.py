from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from typing import List, Optional
from app.schemas.chat import ChatMessage, ChatResponse
from app.services.chat import ChatService
from app.core.security import get_current_user

router = APIRouter()

@router.post("/chat/{knowledge_base_id}", response_model=ChatResponse)
async def chat(
    knowledge_base_id: int,
    message: ChatMessage,
    current_user: Optional[dict] = Depends(get_current_user)
) -> StreamingResponse:
    try:
        return StreamingResponse(
            ChatService.generate_response(
                knowledge_base_id,
                message.content,
                message.session_id
            ),
            media_type="text/event-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{session_id}", response_model=List[ChatMessage])
async def get_chat_history(
    session_id: str,
    current_user: Optional[dict] = Depends(get_current_user)
):
    return ChatService.get_chat_history(session_id)

@router.post("/feedback/{message_id}")
async def provide_feedback(
    message_id: int,
    feedback: str,
    current_user: Optional[dict] = Depends(get_current_user)
):
    return ChatService.save_feedback(message_id, feedback) 