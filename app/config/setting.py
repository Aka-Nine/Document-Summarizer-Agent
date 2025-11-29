from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    ALLOWED_ORIGINS: List[str]
    ALLOWED_HOSTS: List[str]

    MAX_FILE_SIZE: int
    ALLOWED_EXTENSIONS: List[str]
    ALLOWED_MIME_TYPES: List[str]

    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    BUCKET_NAME: str

    DATABASE_URL: str
    REDIS_URL: str

    GROQ_API_KEY: str

    LANGCHAIN_API_KEY: str
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_PROJECT: str = "SmartQABot"

    class Config:
        env_file = ".env"

settings = Settings()
