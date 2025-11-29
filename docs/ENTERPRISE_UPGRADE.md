# Enterprise Document Intelligence Platform (RAG) - Upgrade Guide

## 🚀 What's New

This upgrade transforms the application into an **Enterprise Document Intelligence Platform** with:

### ✨ Key Features

1. **Cloud-Native Architecture**
   - AWS S3, Azure Blob Storage, GCP Cloud Storage support
   - Cloud RDS/PostgreSQL with connection pooling
   - ElastiCache/Redis with SSL support
   - Multi-cloud provider abstraction

2. **RAG (Retrieval Augmented Generation)**
   - Vector database integration (Pinecone, Qdrant, Weaviate, Chroma, OpenSearch)
   - Multiple embedding providers (OpenAI, Cohere, HuggingFace, AWS Bedrock)
   - Intelligent document chunking and retrieval
   - Context-aware Q&A with source citations

3. **Production-Ready Features**
   - API versioning (`/api/v1`)
   - Production middleware (logging, security headers, request IDs)
   - Enhanced error handling and monitoring
   - Database connection pooling
   - Comprehensive metrics and observability

4. **Enhanced Document Processing**
   - Support for PDF, DOCX, TXT, Markdown
   - Advanced chunking strategies
   - RAG-enabled question answering
   - Document query history

## 📁 New File Structure

```
doc-summ-agent/
├── config/
│   └── settings.py          # NEW: Enterprise configuration
├── services/
│   ├── cloud_storage.py      # NEW: Multi-cloud storage
│   ├── embeddings_service.py # NEW: Embeddings providers
│   └── vector_db_service.py   # NEW: Vector database
├── core/
│   ├── rag_processor.py      # NEW: RAG implementation
│   └── enterprise_document_processor.py # NEW: Enterprise processor
├── middleware/
│   └── production.py         # NEW: Production middleware
└── models/
    └── database.py           # UPDATED: RAG support
```

## 🔧 Configuration Changes

### New Environment Variables

#### Cloud Storage
```env
CLOUD_PROVIDER=aws  # aws, azure, gcp, local

# AWS
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_S3_BUCKET_NAME=your-bucket

# Azure (coming soon)
AZURE_STORAGE_ACCOUNT_NAME=...
AZURE_STORAGE_ACCOUNT_KEY=...

# GCP (coming soon)
GCP_PROJECT_ID=...
GCP_STORAGE_BUCKET_NAME=...
```

#### Vector Database
```env
VECTOR_DB_PROVIDER=pinecone  # pinecone, qdrant, weaviate, chroma, opensearch

# Pinecone
PINECONE_API_KEY=your-key
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=documents

# Qdrant
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your-key
QDRANT_COLLECTION_NAME=documents
```

#### Embeddings
```env
EMBEDDING_PROVIDER=openai  # openai, cohere, huggingface, aws_bedrock
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSION=1536

# OpenAI
OPENAI_API_KEY=your-key

# Cohere
COHERE_API_KEY=your-key

# HuggingFace
HUGGINGFACE_API_KEY=your-key
HUGGINGFACE_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
```

#### RAG Configuration
```env
RAG_ENABLED=true
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RETRIEVAL=5
SIMILARITY_THRESHOLD=0.7
RERANK_ENABLED=false
```

#### LLM Providers
```env
LLM_PROVIDER=groq  # groq, openai, anthropic

# Groq
GROQ_API_KEY=your-key
GROQ_MODEL=llama3-8b-8192

# OpenAI
OPENAI_LLM_MODEL=gpt-4-turbo-preview
OPENAI_TEMPERATURE=0.0

# Anthropic
ANTHROPIC_API_KEY=your-key
ANTHROPIC_MODEL=claude-3-opus-20240229
```

#### Production Settings
```env
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
LOG_FORMAT=json
ENABLE_METRICS=true
ENABLE_TRACING=true
API_V1_PREFIX=/api/v1
```

## 📦 New Dependencies

Add to `requirements.txt`:

```txt
# Vector Databases
pinecone-client>=2.2.4
qdrant-client>=1.7.0

# Embeddings
openai>=1.12.0
cohere>=4.37
sentence-transformers>=2.2.2

# Cloud Storage
boto3>=1.34.0  # Already included

# LLM Providers
langchain-openai>=0.1.0
langchain-anthropic>=0.1.0

# Document Processing
python-docx>=1.1.0
```

## 🔄 Migration Steps

### 1. Update Configuration

```bash
# Backup old config
cp config/setting.py config/setting.py.backup

# New config is in config/settings.py
# Update your .env file with new variables
```

### 2. Install New Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Migration

The new models include additional fields. Run migrations:

```python
from models.database import create_tables
create_tables()  # This will add new columns
```

Or use Alembic:
```bash
alembic revision --autogenerate -m "Add RAG support"
alembic upgrade head
```

### 4. Update Imports

Old:
```python
from config.setting import settings
from services.storage_service import StorageService
```

New:
```python
from config.settings import settings
from services.cloud_storage import CloudStorageService
```

### 5. Update Celery Tasks

Update `tasks/celery_tasks.py` to use:
- `EnterpriseDocumentProcessor` instead of `DocumentProcessor`
- `CloudStorageService` instead of `StorageService`

## 🎯 Usage Examples

### Using Cloud Storage

```python
from services.cloud_storage import CloudStorageService

storage = CloudStorageService.create()
object_key = await storage.upload_file(file_content, "document.pdf")
```

### Using RAG

```python
from core.enterprise_document_processor import EnterpriseDocumentProcessor

processor = EnterpriseDocumentProcessor(document_id=123)
result = await processor.process_document(
    file_path="document.pdf",
    questions=["What is this about?"]
)

# Query document
query_result = await processor.query_document(
    query="What are the key findings?",
    document_id=123
)
```

### Using Vector Database

```python
from services.vector_db_service import VectorDBService

vector_db = VectorDBService.create()
await vector_db.create_index(dimension=1536)
```

## 🚨 Breaking Changes

1. **Configuration**: `config/setting.py` → `config/settings.py`
2. **Storage Service**: `StorageService` → `CloudStorageService.create()`
3. **Document Processor**: `DocumentProcessor` → `EnterpriseDocumentProcessor`
4. **Database Models**: New fields added (backward compatible)
5. **API**: New versioned endpoints at `/api/v1`

## 📊 Performance Improvements

- Connection pooling for database
- Async operations for embeddings
- Batch processing for vector operations
- Caching strategies for frequent queries
- Optimized chunking algorithms

## 🔒 Security Enhancements

- Security headers middleware
- Request ID tracking
- Enhanced logging
- Rate limiting improvements
- Input validation

## 📈 Monitoring & Observability

- Structured logging (JSON format)
- Request/response tracking
- Performance metrics
- Error tracking
- Health check endpoints

## 🆘 Support

For issues or questions:
1. Check configuration in `config/settings.py`
2. Review logs for detailed error messages
3. Verify cloud service credentials
4. Test vector database connectivity

---

**Next Steps:**
1. Update your `.env` file
2. Install new dependencies
3. Run database migrations
4. Test with sample documents
5. Deploy to production

