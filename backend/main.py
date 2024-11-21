from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat, knowledge
from app.core.config import settings
from app.db.session import engine
from app.models import Base

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HR Knowledge Base API",
    description="HR Knowledge Base Backend API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(chat.router, prefix=f"{settings.API_V1_STR}/chat", tags=["chat"])
app.include_router(knowledge.router, prefix=f"{settings.API_V1_STR}/knowledge", tags=["knowledge"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 