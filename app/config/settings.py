"""
Enterprise Document Intelligence Platform - Configuration
Production-ready settings with cloud service support
"""
from pydantic_settings import BaseSettings
from typing import List, Optional
from enum import Enum


class CloudProvider(str, Enum):
    """Supported cloud providers"""
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    LOCAL = "local"  # MinIO (requires Docker)
    FILESYSTEM = "filesystem"  # Local filesystem (no Docker needed)


class VectorDBProvider(str, Enum):
    """Supported vector database providers"""
    PINECONE = "pinecone"
    QDRANT = "qdrant"
    WEAVIATE = "weaviate"
    CHROMA = "chroma"
    OPENSEARCH = "opensearch"


class EmbeddingProvider(str, Enum):
    """Supported embedding providers"""
    OPENAI = "openai"
    COHERE = "cohere"
    HUGGINGFACE = "huggingface"
    AWS_BEDROCK = "aws_bedrock"
    GROQ = "groq"


class Settings(BaseSettings):
    """Application settings with cloud service support"""
    
    # Application
    APP_NAME: str = "Enterprise Document Intelligence Platform"
    APP_VERSION: str = "2.0.0"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"  # production, staging, development
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS and Security
    ALLOWED_ORIGINS: List[str] = ["*"]
    ALLOWED_HOSTS: List[str] = ["*"]
    TRUSTED_PROXIES: List[str] = ["127.0.0.1", "localhost"]
    
    # File Upload
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB default
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".docx", ".txt", ".md"]
    ALLOWED_MIME_TYPES: List[str] = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain",
        "text/markdown"
    ]
    
    # Cloud Provider Selection
    CLOUD_PROVIDER: CloudProvider = CloudProvider.FILESYSTEM  # Default to filesystem (no Docker)
    
    # AWS Configuration
    AWS_REGION: Optional[str] = None
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_S3_BUCKET_NAME: Optional[str] = None
    AWS_S3_ENDPOINT_URL: Optional[str] = None  # For S3-compatible services
    
    # Azure Configuration
    AZURE_STORAGE_ACCOUNT_NAME: Optional[str] = None
    AZURE_STORAGE_ACCOUNT_KEY: Optional[str] = None
    AZURE_STORAGE_CONTAINER_NAME: Optional[str] = None
    AZURE_STORAGE_CONNECTION_STRING: Optional[str] = None
    
    # GCP Configuration
    GCP_PROJECT_ID: Optional[str] = None
    GCP_STORAGE_BUCKET_NAME: Optional[str] = None
    GCP_CREDENTIALS_PATH: Optional[str] = None
    
    # Local/MinIO (for development)
    MINIO_ENDPOINT: Optional[str] = None
    MINIO_ACCESS_KEY: Optional[str] = None
    MINIO_SECRET_KEY: Optional[str] = None
    BUCKET_NAME: Optional[str] = None
    
    # Filesystem Storage (no Docker needed)
    FILESYSTEM_STORAGE_PATH: str = "storage"  # Local directory for file storage
    FILESYSTEM_BASE_URL: str = "http://localhost:8000/files"  # Base URL for file access
    
    # MongoDB Configuration
    MONGODB_URL: str = "mongodb+srv://Nine:2xGBEpr60Yde3M8m@ninecluster.ltpa6.mongodb.net/?appName=NIneCluster"  # MongoDB connection string
    MONGODB_DB_NAME: str = "doc_intelligence"  # Database name
    
    # Database Connection Pooling (for MongoDB)
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    DATABASE_POOL_PRE_PING: bool = True
    DATABASE_ECHO: bool = False
    
    # Redis Configuration
    REDIS_PROVIDER: str = "redis_cloud"  # redis, redis_cloud
    REDIS_URL: Optional[str] = None  # Redis connection URL (standard or Redis Cloud)
    
    # Redis Cloud Configuration (if using Redis Cloud Console)
    REDIS_CLOUD_ENDPOINT: Optional[str] = None  # e.g., redis-12345.c1.us-east-1-1.ec2.cloud.redislabs.com
    REDIS_CLOUD_PORT: int = 14497
    REDIS_CLOUD_USERNAME: str = "default"  # Redis Cloud username
    REDIS_CLOUD_PASSWORD: Optional[str] = None
    
    # Standard Redis (fallback)
    REDIS_HOST: Optional[str] = None
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_SSL: bool = False
    REDIS_DB: int = 0
    
    # Vector Database Configuration
    VECTOR_DB_PROVIDER: VectorDBProvider = VectorDBProvider.CHROMA
    VECTOR_DB_INDEX_NAME: str = "document-intelligence"
    
    # Pinecone
    PINECONE_API_KEY: Optional[str] = None
    PINECONE_ENVIRONMENT: Optional[str] = None
    PINECONE_INDEX_NAME: Optional[str] = None
    
    # Qdrant
    QDRANT_URL: Optional[str] = None
    QDRANT_API_KEY: Optional[str] = None
    QDRANT_COLLECTION_NAME: Optional[str] = None
    
    # Weaviate
    WEAVIATE_URL: Optional[str] = None
    WEAVIATE_API_KEY: Optional[str] = None
    WEAVIATE_CLASS_NAME: Optional[str] = None
    
    # Chroma
    CHROMA_PERSIST_DIR: Optional[str] = "./chroma_db"
    CHROMA_API_KEY: Optional[str] = None
    CHROMA_TENANT: Optional[str] = None
    CHROMA_DATABASE: Optional[str] = None
    CHROMA_SERVER_HOST: Optional[str] = None  # For Chroma Cloud endpoint
    CHROMA_SERVER_PORT: int = 8000
    
    # OpenSearch
    OPENSEARCH_URL: Optional[str] = None
    OPENSEARCH_USERNAME: Optional[str] = None
    OPENSEARCH_PASSWORD: Optional[str] = None
    
    # Embeddings Configuration
    EMBEDDING_PROVIDER: EmbeddingProvider = EmbeddingProvider.OPENAI
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    EMBEDDING_DIMENSION: int = 1536
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_ORG_ID: Optional[str] = None
    
    # Cohere
    COHERE_API_KEY: Optional[str] = None
    
    # HuggingFace
    HUGGINGFACE_API_KEY: Optional[str] = None
    HUGGINGFACE_MODEL_NAME: Optional[str] = "sentence-transformers/all-MiniLM-L6-v2"
    
    # AWS Bedrock
    AWS_BEDROCK_MODEL_ID: Optional[str] = "amazon.titan-embed-text-v1"
    
    # LLM Configuration
    LLM_PROVIDER: str = "gemini"  # gemini, groq, openai, anthropic, aws_bedrock
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "llama3-8b-8192"
    
    OPENAI_LLM_MODEL: str = "gpt-4-turbo-preview"
    OPENAI_TEMPERATURE: float = 0.0
    
    ANTHROPIC_API_KEY: Optional[str] = None
    ANTHROPIC_MODEL: str = "claude-3-opus-20240229"
    
    # Google Gemini
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-pro"  # or gemini-pro-vision, gemini-1.5-pro
    
    # RAG Configuration
    RAG_ENABLED: bool = True
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TOP_K_RETRIEVAL: int = 5
    SIMILARITY_THRESHOLD: float = 0.7
    RERANK_ENABLED: bool = False
    RERANK_MODEL: Optional[str] = None
    
    # LangChain
    LANGCHAIN_API_KEY: Optional[str] = None
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_PROJECT: str = "Enterprise-Document-Intelligence"
    LANGCHAIN_ENDPOINT: Optional[str] = None
    
    # Monitoring & Observability
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    ENABLE_TRACING: bool = True
    LOG_LEVEL: str = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_FORMAT: str = "json"  # json, text
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_UPLOAD_PER_MINUTE: int = 5
    
    # Celery Configuration
    CELERY_BROKER_URL: Optional[str] = None  # Override REDIS_URL if needed
    CELERY_RESULT_BACKEND: Optional[str] = None
    CELERY_TASK_SERIALIZER: str = "json"
    CELERY_RESULT_SERIALIZER: str = "json"
    CELERY_ACCEPT_CONTENT: List[str] = ["json"]
    CELERY_TIMEZONE: str = "UTC"
    CELERY_ENABLE_UTC: bool = True
    CELERY_TASK_TRACK_STARTED: bool = True
    CELERY_TASK_TIME_LIMIT: int = 300  # 5 minutes
    CELERY_TASK_SOFT_TIME_LIMIT: int = 240  # 4 minutes
    
    # Retry Configuration
    MAX_RETRIES: int = 3
    RETRY_BACKOFF_FACTOR: float = 2.0
    RETRY_MAX_WAIT: int = 60
    
    # Health Check
    HEALTH_CHECK_INTERVAL: int = 30  # seconds
    
    class Config:
        # Allow overriding the path to an env file via the ENV_FILE_PATH environment variable.
        # If ENV_FILE_PATH is not set, do not force-loading a file so that container/compose
        # provided environment variables take precedence.
        import os
        env_file = os.getenv("ENV_FILE_PATH", None)
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()

