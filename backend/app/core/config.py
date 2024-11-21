from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any
from pydantic import PostgresDsn, validator
import secrets

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # MySQL配置
    MYSQL_SERVER: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    # Redis配置
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    
    # 知识库配置
    VECTOR_STORE_PATH: str = "vector_store"
    MODEL_NAME: str = "moonshot_proxyllm"
    
    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return f"mysql+pymysql://{values.get('MYSQL_USER')}:{values.get('MYSQL_PASSWORD')}@{values.get('MYSQL_SERVER')}/{values.get('MYSQL_DB')}"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 