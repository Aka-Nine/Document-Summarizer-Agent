"""
Enterprise Document Intelligence Platform - Database Models
Production-ready database models with RAG support
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, JSON, Enum, Boolean, Float, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from sqlalchemy.pool import QueuePool
import enum
import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from app.config.settings import settings
except ImportError:
    from app.config.setting import settings

# Get database URL from service
try:
    from app.services.database_service import DatabaseService
    DATABASE_URL = DatabaseService.get_connection_url()
    import structlog
    db_logger = structlog.get_logger()
    db_logger.info("Database connection configured", **DatabaseService.get_connection_info())
except Exception as e:
    # Fallback to direct DATABASE_URL or environment
    DATABASE_URL = os.getenv("DATABASE_URL", getattr(settings, "DATABASE_URL", None))
    if not DATABASE_URL:
        # Final fallback: use default Docker Compose database URL
        DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/docprocessing"
        import warnings
        warnings.warn("Using default database URL. Configure DATABASE_PROVIDER in settings.")

# Production-ready engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=settings.DATABASE_POOL_PRE_PING,
    echo=settings.DATABASE_ECHO,
    connect_args={
        "connect_timeout": 10,
        "application_name": "doc_intelligence_platform"
    }
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,  # Important for Celery tasks
    bind=engine
)

Base = declarative_base()


class ProcessingStatus(enum.Enum):
    """Document processing status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    INDEXED = "indexed"  # Indexed in vector DB


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    
    # Relationships
    documents = relationship("Document", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"


class Document(Base):
    """Document model with RAG support"""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False, index=True)
    file_size = Column(Integer, nullable=False)
    file_type = Column(String, nullable=True)  # pdf, docx, txt, etc.
    mime_type = Column(String, nullable=True)
    
    # Processing status
    status = Column(Enum(ProcessingStatus), default=ProcessingStatus.PENDING, nullable=False, index=True)
    
    # Content
    summary = Column(Text, nullable=True)
    qa_results = Column(JSON, nullable=True)  # Store Q&A results as JSON
    
    # RAG metadata
    rag_enabled = Column(Boolean, default=True, nullable=False)
    chunks_indexed = Column(Integer, default=0, nullable=False)
    vector_db_indexed = Column(Boolean, default=False, nullable=False)
    
    # Processing metadata
    processing_time = Column(Float, nullable=True)  # in seconds
    error_message = Column(Text, nullable=True)
    error_traceback = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    processed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="documents")
    queries = relationship("DocumentQuery", back_populates="document", cascade="all, delete-orphan")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_documents_user_status', 'user_id', 'status'),
        Index('idx_documents_created', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Document(id={self.id}, filename={self.filename}, status={self.status.value})>"


class DocumentQuery(Base):
    """Document query history for RAG"""
    __tablename__ = "document_queries"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    query = Column(Text, nullable=False)
    answer = Column(Text, nullable=True)
    
    # RAG metadata
    context_chunks_used = Column(Integer, default=0, nullable=False)
    similarity_scores = Column(JSON, nullable=True)  # Store similarity scores
    retrieval_method = Column(String, default="vector_search", nullable=False)
    
    # Performance metrics
    response_time = Column(Float, nullable=True)  # in seconds
    tokens_used = Column(Integer, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    # Relationships
    document = relationship("Document", back_populates="queries")
    
    # Indexes
    __table_args__ = (
        Index('idx_queries_document_created', 'document_id', 'created_at'),
    )
    
    def __repr__(self):
        return f"<DocumentQuery(id={self.id}, document_id={self.document_id}, query={self.query[:50]}...)>"


class SystemMetrics(Base):
    """System metrics and monitoring"""
    __tablename__ = "system_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String, nullable=False, index=True)
    metric_value = Column(Float, nullable=False)
    metric_type = Column(String, nullable=False)  # counter, gauge, histogram
    tags = Column(JSON, nullable=True)  # Additional metadata
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    __table_args__ = (
        Index('idx_metrics_name_timestamp', 'metric_name', 'timestamp'),
    )


def create_tables():
    """Create all database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"⚠️ Warning: Could not create database tables: {e}")
        print("This is normal if the database is not available yet")
