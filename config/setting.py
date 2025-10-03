from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS and Security
    ALLOWED_ORIGINS: List[str] = ["*"]
    ALLOWED_HOSTS: List[str] = ["*"]

    # File Upload Settings
    MAX_FILE_SIZE: int = 10485760  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".txt", ".docx"]
    ALLOWED_MIME_TYPES: List[str] = ["application/pdf", "text/plain", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]

    # AWS Configuration
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str = "us-east-1"
    
    # S3 Configuration
    S3_BUCKET_NAME: str
    
    # DynamoDB Configuration
    DYNAMODB_CACHE_TABLE: str = "document-cache"
    
    # ElastiCache Configuration (Optional)
    ELASTICACHE_ENDPOINT: Optional[str] = None
    
    # SQS Configuration
    SQS_QUEUE_NAME: str = "document-processing-queue"
    SQS_QUEUE_URL: Optional[str] = None
    
    # Lambda Configuration
    LAMBDA_FUNCTION_NAME: Optional[str] = None
    
    # Database Configuration
    DATABASE_URL: str
    
    # Legacy Redis (for backward compatibility)
    REDIS_URL: Optional[str] = None

    # AI Configuration
    GROQ_API_KEY: str
    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_PROJECT: str = "DocumentSummarizerAgent"

    # Rate Limiting
    UPLOAD_RATE_LIMIT: int = 2  # uploads per minute
    MAX_PROCESSING_TIME: int = 300  # 5 minutes timeout

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
