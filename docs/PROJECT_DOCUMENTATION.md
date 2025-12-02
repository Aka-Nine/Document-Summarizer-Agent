# Enterprise Document Intelligence Platform - Complete Documentation

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Key Features](#key-features)
4. [Technology Stack](#technology-stack)
5. [Project Structure](#project-structure)
6. [Core Components](#core-components)
7. [Setup & Configuration](#setup--configuration)
8. [API Endpoints](#api-endpoints)
9. [Database Models](#database-models)
10. [Services](#services)
11. [Background Tasks](#background-tasks)
12. [Security & Authentication](#security--authentication)
13. [Performance & Scaling](#performance--scaling)
14. [Deployment](#deployment)
15. [Troubleshooting](#troubleshooting)

---

## Project Overview

### What is this Project?

The **Enterprise Document Intelligence Platform** is a production-ready, cloud-native application designed to process, analyze, and retrieve information from documents using advanced AI capabilities. It combines:

- **Document Processing**: Automatically extract, chunk, and analyze document content
- **Semantic Search**: Find relevant information using vector embeddings and similarity matching
- **RAG (Retrieval-Augmented Generation)**: Enhance LLM responses with retrieved document context
- **Cloud Integration**: Works seamlessly with cloud services (MongoDB, Redis, Chroma, AWS, Azure, GCP)
- **Enterprise Features**: Production middleware, monitoring, logging, rate limiting, and scalability

### Target Use Cases

- **Document Search**: Semantic search across document libraries
- **Intelligent Summarization**: AI-powered document summaries
- **Question Answering**: Answer questions based on document content
- **Content Analysis**: Extract insights and patterns from documents
- **Knowledge Management**: Build searchable knowledge bases from documents

### Key Statistics

- **Language**: Python 3.12+
- **Framework**: FastAPI (async)
- **Database**: MongoDB + Chroma Vector DB
- **Message Queue**: Redis (via Celery)
- **LLM Support**: Gemini, Groq, OpenAI, Anthropic, AWS Bedrock
- **Deployment**: Docker, Kubernetes, or standalone

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT APPLICATIONS                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │   Web UI     │    │   Mobile     │    │   API Client │   │
│  └──────────────┘    └──────────────┘    └──────────────┘   │
│                            ▼                                  │
├─────────────────────────────────────────────────────────────┤
│                    NGINX REVERSE PROXY                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         FASTAPI APPLICATION (Async)                 │   │
│  │  ┌──────────────────────────────────────────────┐  │   │
│  │  │  API Routes (v1)                             │  │   │
│  │  │  - Document Upload/Processing               │  │   │
│  │  │  - Search                                    │  │   │
│  │  │  - Question Answering                        │  │   │
│  │  │  - User Management                           │  │   │
│  │  └──────────────────────────────────────────────┘  │   │
│  │                      ▼                              │   │
│  │  ┌──────────────────────────────────────────────┐  │   │
│  │  │  Business Logic Layer                        │  │   │
│  │  │  - EnterpriseDocumentProcessor               │  │   │
│  │  │  - RAGProcessor                              │  │   │
│  │  │  - MongoDB Models                            │  │   │
│  │  └──────────────────────────────────────────────┘  │   │
│  │                      ▼                              │   │
│  │  ┌──────────────────────────────────────────────┐  │   │
│  │  │  Services Layer                              │  │   │
│  │  │  - Vector DB Service (Chroma Cloud)          │  │   │
│  │  │  - Embeddings Service (HuggingFace)          │  │   │
│  │  │  - Redis Service (Caching)                   │  │   │
│  │  │  - AWS/Storage Service                       │  │   │
│  │  └──────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │    CELERY WORKER (Background Tasks)                 │   │
│  │  - Document Processing                             │   │
│  │  - Embedding Generation                            │   │
│  │  - Vector Indexing                                 │   │
│  │  - Async Operations                                │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│                     DATA & SERVICES LAYER                    │
│                                                               │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │   MongoDB    │ │   Redis      │ │   Chroma     │        │
│  │   (Database) │ │   (Cache)    │ │   (Vectors)  │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
│                                                               │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │  AWS S3 /    │ │  HuggingFace │ │  Gemini/     │        │
│  │  MinIO/FS    │ │  Embeddings  │ │  Groq LLM    │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

```
Document Upload
      ▼
┌─────────────────────┐
│ File Validation     │
│ Storage            │  ──► File Storage (S3/MinIO/Filesystem)
└─────────────────────┘
      ▼
┌─────────────────────┐
│ Celery Task Queue   │  ──► Redis Queue
└─────────────────────┘
      ▼
┌─────────────────────┐
│ Celery Worker       │
│ - Extract Text     │
│ - Chunk Document   │
└─────────────────────┘
      ▼
┌─────────────────────────┐
│ Generate Embeddings     │  ──► HuggingFace API
│ (Vector Representations)│
└─────────────────────────┘
      ▼
┌─────────────────────────┐
│ Index in Vector DB      │  ──► Chroma Cloud
│ Store Metadata          │  ──► MongoDB
└─────────────────────────┘
      ▼
Ready for Search & RAG
      │
      ├─► Semantic Search
      ├─► Question Answering
      └─► Summary Generation
```

---

## Key Features

### 1. **RAG (Retrieval-Augmented Generation)**
- Semantic search across document collections
- Context-aware responses from LLM
- Relevance scoring and filtering
- Multi-document synthesis

### 2. **Multi-LLM Support**
- **Gemini** (Primary - best for multi-modal)
- **Groq** (Fast inference, great for chat)
- **OpenAI** (Most capable)
- **Anthropic Claude** (Strong reasoning)
- **AWS Bedrock** (Enterprise integration)

### 3. **Multiple Vector Databases**
- **Chroma** (Cloud - configured with your credentials)
- **Pinecone** (Fully managed, fast)
- **Qdrant** (Self-hosted, powerful)
- **Weaviate** (Extensible)
- **OpenSearch** (AWS-integrated)

### 4. **Document Format Support**
- PDF files
- Word documents (.docx)
- Plain text (.txt)
- Markdown (.md)

### 5. **Enterprise Features**
- **Authentication**: JWT-based auth
- **Rate Limiting**: Prevent abuse
- **Logging**: Structured, JSON-formatted
- **Monitoring**: Prometheus metrics
- **Health Checks**: Service health endpoints
- **Error Handling**: Comprehensive error management

### 6. **Production Scalability**
- **Async/Await**: FastAPI with full async support
- **Background Tasks**: Celery for heavy processing
- **Caching**: Redis for performance
- **Connection Pooling**: MongoDB connection pooling
- **Load Balancing**: Nginx reverse proxy

### 7. **Cloud-Native**
- **Docker Support**: Containerized deployment
- **Kubernetes Ready**: Full K8s config included
- **Multi-Cloud**: AWS, Azure, GCP support
- **Environment-Based Config**: 12-factor app compliant

---

## Technology Stack

### Backend Framework
| Component | Technology | Version |
|-----------|-----------|---------|
| Web Framework | FastAPI | 0.111.0 |
| ASGI Server | Uvicorn | 0.30.6 |
| Language | Python | 3.12+ |

### Databases
| Component | Technology | Purpose |
|-----------|-----------|---------|
| Primary DB | MongoDB | Document & metadata storage |
| Vector DB | Chroma | Vector embeddings & similarity search |
| Cache | Redis | Task queue, caching, sessions |

### LLM & NLP
| Component | Technology | Purpose |
|-----------|-----------|---------|
| LLM Framework | LangChain | LLM orchestration |
| Embeddings | HuggingFace | Vector representations |
| LLM Providers | Multiple | Gemini, Groq, OpenAI, Anthropic |

### Document Processing
| Component | Technology | Purpose |
|-----------|-----------|---------|
| PDF Processing | PyPDF | PDF text extraction |
| Word Processing | Python-DOCX | .docx file handling |
| Chunking | LangChain | Intelligent text splitting |

### Task Queue & Scheduling
| Component | Technology | Purpose |
|-----------|-----------|---------|
| Task Queue | Celery | Background job processing |
| Broker | Redis | Message broker for Celery |
| Monitoring | Flower | Celery task monitoring |

### Security & Auth
| Component | Technology | Purpose |
|-----------|-----------|---------|
| JWT | python-jose | Token generation/validation |
| Password Hashing | bcrypt | Secure password storage |
| Rate Limiting | SlowAPI | API rate limiting |

### Infrastructure
| Component | Technology | Purpose |
|-----------|-----------|---------|
| Containerization | Docker | Application containers |
| Orchestration | Kubernetes | Container orchestration |
| Reverse Proxy | Nginx | Load balancing, SSL |
| File Storage | S3/MinIO/FS | Document storage |

### Monitoring & Logging
| Component | Technology | Purpose |
|-----------|-----------|---------|
| Logging | Structlog | Structured logging |
| Metrics | Prometheus | Performance metrics |
| Tracing | LangChain | LLM call tracing |

---

## Project Structure

```
doc-summ-agent/
├── app/                          # Main application package
│   ├── __init__.py
│   ├── api/
│   │   ├── main.py              # FastAPI app initialization
│   │   └── v1/
│   │       ├── routes_mongodb.py # API endpoints
│   │       └── __init__.py
│   │
│   ├── config/
│   │   ├── settings.py          # Pydantic settings configuration
│   │   └── __init__.py
│   │
│   ├── core/
│   │   ├── enterprise_document_processor.py  # Document processing logic
│   │   ├── rag_processor.py      # RAG implementation
│   │   └── __init__.py
│   │
│   ├── middleware/
│   │   ├── production.py         # Production middleware setup
│   │   └── __init__.py
│   │
│   ├── models/
│   │   ├── mongodb_database.py   # MongoDB collections & schemas
│   │   └── __init__.py
│   │
│   ├── services/
│   │   ├── vector_db_service.py  # Vector DB abstraction
│   │   ├── embeddings_service.py # Embeddings generation
│   │   ├── redis_service.py      # Redis client
│   │   ├── aws_cache_service.py  # AWS caching
│   │   ├── aws_task_service.py   # AWS task integration
│   │   ├── cloud_storage.py      # Multi-cloud storage
│   │   └── __init__.py
│   │
│   ├── tasks/
│   │   ├── celery_tasks.py       # Celery task definitions
│   │   └── __init__.py
│   │
│   └── utils/
│       ├── logger.py             # Logging utilities
│       └── __init__.py
│
├── scripts/                      # Utility scripts
│   ├── start_server.py          # Start FastAPI server
│   ├── celery_worker.py         # Start Celery worker
│   ├── check_system.py          # System health check
│   ├── setup_env.py             # Environment setup
│   ├── run_report_processor.py  # Report processing
│   ├── check_and_start.py       # Combined checks
│   └── backup/                  # Script backups
│
├── tests/                        # Test suite
│   ├── conftest.py              # Pytest configuration
│   ├── test_imports.py          # Import tests
│   ├── test_config.py           # Configuration tests
│   ├── unit/                    # Unit tests
│   ├── integration/             # Integration tests
│   └── README.md                # Test documentation
│
├── infra/                       # Infrastructure configs
│   ├── docker/                  # Docker setup
│   ├── k8s/                     # Kubernetes manifests
│   ├── nginx/                   # Nginx configs
│   ├── ssl/                     # SSL certificates
│   ├── terraform/               # Terraform IaC
│   ├── monitoring/              # Prometheus configs
│   └── logs/                    # Log configurations
│
├── frontend/                    # Frontend application
│   ├── index.html
│   └── README.md
│
├── archive_root/                # Archived legacy scripts
│   └── (preserved original scripts)
│
├── storage/                     # Local file storage
│   └── (uploaded documents)
│
├── chroma_db/                   # Local Chroma DB (if using local)
│   └── chroma.sqlite3
│
├── logs/                        # Application logs
│   └── (*.log files)
│
├── .env                         # Production environment (KEEP SECRET!)
├── .env.example                 # Environment template
├── config.env                   # Additional configuration
├── docker-compose.yml           # Docker Compose orchestration
├── Dockerfile                   # Docker image definition
├── requirements.txt             # Python dependencies
├── requirements-test.txt        # Test dependencies
├── pytest.ini                   # Pytest configuration
├── run.py                       # Main entry point
├── Readme.md                    # Quick start guide
└── PROJECT_DOCUMENTATION.md     # This file
```

---

## Core Components

### 1. FastAPI Application (`app/api/main.py`)

**Purpose**: Main application initialization and route configuration

**Key Features**:
```python
- FastAPI app with OpenAPI documentation
- Production middleware setup
- MongoDB connection initialization
- Rate limiting configuration
- Frontend static file mounting
- Startup/shutdown event handlers
```

**Main Routes** (from `v1/routes_mongodb.py`):
```
POST   /api/v1/documents/upload      - Upload a document
GET    /api/v1/documents/{doc_id}    - Get document
DELETE /api/v1/documents/{doc_id}    - Delete document
GET    /api/v1/documents/search      - Search documents
POST   /api/v1/chat                  - Chat with RAG
POST   /api/v1/summarize             - Generate summary
POST   /api/v1/auth/register         - User registration
POST   /api/v1/auth/login            - User login
```

### 2. Enterprise Document Processor (`app/core/enterprise_document_processor.py`)

**Purpose**: Core document processing and LLM orchestration

**Key Methods**:
```python
process_document()          # Extract and process document
generate_summary()          # Create document summary
answer_question()          # QA with RAG
extract_entities()         # Extract named entities
analyze_sentiment()        # Analyze document sentiment
```

**Supported LLM Providers**:
- Groq (Fast inference)
- OpenAI (GPT-4)
- Anthropic (Claude)
- Google Gemini (Multi-modal)
- AWS Bedrock (Enterprise)

### 3. RAG Processor (`app/core/rag_processor.py`)

**Purpose**: Implement Retrieval-Augmented Generation

**Key Methods**:
```python
index_document()           # Index document chunks
retrieve_context()         # Find relevant chunks
generate_answer()         # Generate answer with context
rerank_results()          # Rerank results by relevance
```

**Process Flow**:
1. Split document into chunks
2. Generate embeddings for each chunk
3. Index embeddings in vector database
4. Retrieve relevant chunks for queries
5. Pass chunks as context to LLM

### 4. Vector DB Service (`app/services/vector_db_service.py`)

**Purpose**: Abstract interface for multiple vector databases

**Supported Providers**:
- **Chroma** (Your configured provider - Cloud)
- Pinecone (Fully managed)
- Qdrant (Self-hosted)
- Weaviate
- OpenSearch

**Key Methods**:
```python
create_index()             # Create vector index
upsert_vectors()          # Store vectors
search()                  # Semantic search
delete_vectors()          # Remove vectors
get_stats()               # Index statistics
```

**Current Configuration**:
```
Provider: Chroma Cloud
API Key: ●●●●●●●●●●●●●iUwo
Tenant: dc494ac1-d8ba-495c-9853-563b59f2fb88
Database: User-Data
Collection: document-intelligence
```

### 5. Embeddings Service (`app/services/embeddings_service.py`)

**Purpose**: Generate vector embeddings for text

**Supported Providers**:
- HuggingFace (Free, no API key)
- OpenAI (Powerful, paid)
- Cohere (Great for semantic search)
- AWS Bedrock (Enterprise)

**Key Methods**:
```python
embed()                   # Single text embedding
embed_batch()            # Batch embeddings
get_dimension()          # Embedding dimension
```

### 6. MongoDB Models (`app/models/mongodb_database.py`)

**Purpose**: Define data schemas and collections

**Collections**:
```python
users              # User accounts
documents          # Document metadata
chunks             # Document chunks
embeddings         # Embedding metadata
search_history     # Search logs
api_logs          # API request logs
```

**Key Models**:
```python
User               # Authentication
Document          # Document metadata
DocumentChunk     # Text chunks
EmbeddingRecord   # Vector metadata
```

### 7. Celery Tasks (`app/tasks/celery_tasks.py`)

**Purpose**: Background job processing

**Key Tasks**:
```python
process_document_task()    # Process uploaded document
generate_embeddings_task() # Generate vector embeddings
index_vectors_task()       # Index in vector database
cleanup_old_data()         # Maintenance tasks
```

---

## Setup & Configuration

### Prerequisites

```bash
# System Requirements
- Python 3.12+
- pip/conda package manager
- MongoDB Atlas (or local MongoDB)
- Redis Cloud (or local Redis)
- Internet connection (for cloud services)

# Optional
- Docker & Docker Compose
- Kubernetes cluster
- AWS/Azure/GCP account
```

### Installation

```bash
# 1. Clone repository
git clone https://github.com/Aka-Nine/Document-Summarizer-Agent.git
cd doc-summ-agent

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
python -m pip install "pymongo[srv]"

# 4. Create .env file
cp env.example .env

# 5. Configure environment variables
# Edit .env with your credentials
nano .env  # or use your favorite editor
```

### Environment Configuration

**Critical Settings** (required for operation):

```env
# Security
SECRET_KEY=<generate-with-openssl-rand-hex-32>
ALGORITHM=HS256

# MongoDB (Database)
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/?appName=app
MONGODB_DB_NAME=doc_intelligence

# Redis Cloud (Message Queue)
REDIS_CLOUD_ENDPOINT=redis-xxxxx.ec2.cloud.redislabs.com
REDIS_CLOUD_PORT=12345
REDIS_CLOUD_PASSWORD=your_password

# LLM Provider (Primary)
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key

# Chroma Vector DB (Configured)
CHROMA_API_KEY=ck-GZZ6cKpGpFSWsoAYbGCrXJKzzkAR84tv3BSU5KTHiUwo
CHROMA_TENANT=dc494ac1-d8ba-495c-9853-563b59f2fb88
CHROMA_DATABASE=User-Data

# Embeddings
EMBEDDING_PROVIDER=huggingface
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

**Optional Settings**:

```env
# Alternative LLM Providers
GROQ_API_KEY=gsk_xxxxx
OPENAI_API_KEY=sk_xxxxx
ANTHROPIC_API_KEY=sk_xxxxx

# Alternative Vector DBs
PINECONE_API_KEY=xxxxx
QDRANT_URL=http://localhost:6333

# Cloud Storage
CLOUD_PROVIDER=filesystem  # or: aws, azure, gcp
AWS_S3_BUCKET_NAME=my-bucket

# Monitoring
ENABLE_TRACING=true
LOG_LEVEL=INFO
```

### Running the Application

**Option 1: Local Development**

```bash
# Terminal 1: Start FastAPI server
python run.py
# Access at http://localhost:8000

# Terminal 2: Start Celery worker
celery -A app.tasks.celery_tasks worker --loglevel=info

# Terminal 3 (Optional): Start Flower (task monitor)
celery -A app.tasks.celery_tasks flower --port=5555
# Access at http://localhost:5555
```

**Option 2: Docker Compose**

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop all services
docker-compose down
```

**Option 3: Kubernetes**

```bash
# Deploy to Kubernetes
kubectl apply -f infra/k8s/

# Check deployment
kubectl get pods
kubectl get services

# View logs
kubectl logs -f deployment/api
```

### Testing Configuration

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_services.py

# Run with coverage
pytest --cov=app

# Run integration tests
pytest tests/integration/ -v
```

---

## API Endpoints

### Authentication

```
POST /api/v1/auth/register
Body: {
  "username": "user@example.com",
  "password": "secure_password",
  "full_name": "John Doe"
}
Response: {
  "user_id": "uuid",
  "username": "user@example.com",
  "token": "jwt_token"
}

POST /api/v1/auth/login
Body: {
  "username": "user@example.com",
  "password": "secure_password"
}
Response: {
  "access_token": "jwt_token",
  "token_type": "bearer"
}
```

### Document Management

```
POST /api/v1/documents/upload
Headers: Authorization: Bearer {token}
Body: FormData {
  "file": <binary>,
  "title": "Document Title",
  "description": "Optional description"
}
Response: {
  "document_id": "uuid",
  "title": "Document Title",
  "status": "processing",
  "created_at": "2025-11-30T..."
}

GET /api/v1/documents/{document_id}
Response: {
  "document_id": "uuid",
  "title": "Document Title",
  "content_preview": "First 500 chars...",
  "chunks_count": 42,
  "indexed": true,
  "created_at": "2025-11-30T..."
}

DELETE /api/v1/documents/{document_id}
Response: {
  "status": "deleted",
  "document_id": "uuid"
}

GET /api/v1/documents
Query: ?page=1&page_size=20
Response: {
  "documents": [...],
  "total": 150,
  "page": 1,
  "page_size": 20
}
```

### Search & Retrieval

```
GET /api/v1/search
Query: ?q=search_term&top_k=5
Response: {
  "results": [
    {
      "document_id": "uuid",
      "chunk_id": "uuid",
      "text": "Relevant chunk...",
      "score": 0.95,
      "metadata": {...}
    }
  ],
  "search_time_ms": 245
}
```

### Chat & QA

```
POST /api/v1/chat
Body: {
  "message": "What is the main topic of this document?",
  "document_id": "uuid",
  "conversation_id": "uuid"
}
Response: {
  "response": "The main topic is...",
  "sources": [
    {
      "chunk_id": "uuid",
      "text": "Source text...",
      "score": 0.92
    }
  ],
  "processing_time_ms": 1250
}

POST /api/v1/summarize
Body: {
  "document_id": "uuid",
  "summary_length": "medium"  # short, medium, long
}
Response: {
  "summary": "Document summary...",
  "word_count": 150,
  "key_points": [...]
}
```

### Analytics

```
GET /api/v1/analytics/search-history
Query: ?user_id=uuid&days=30
Response: {
  "total_searches": 245,
  "top_queries": [...],
  "search_trends": [...]
}

GET /api/v1/health
Response: {
  "status": "healthy",
  "database": "connected",
  "redis": "connected",
  "vector_db": "connected",
  "uptime_seconds": 3600
}
```

---

## Database Models

### Users Collection

```javascript
{
  _id: ObjectId,
  username: string (unique),
  email: string (unique),
  password_hash: string,
  full_name: string,
  created_at: timestamp,
  updated_at: timestamp,
  is_active: boolean,
  subscription_tier: "free" | "pro" | "enterprise",
  storage_quota_mb: number,
  api_calls_limit: number
}
```

### Documents Collection

```javascript
{
  _id: ObjectId,
  user_id: ObjectId,
  filename: string,
  title: string,
  description: string,
  file_path: string,
  file_size_bytes: number,
  content_type: string,
  status: "pending" | "processing" | "indexed" | "failed",
  chunks_count: number,
  text_content: string (preview),
  tags: [string],
  created_at: timestamp,
  updated_at: timestamp,
  processed_at: timestamp,
  vector_indexed: boolean,
  metadata: {
    pages: number,
    language: string,
    summary: string
  }
}
```

### Chunks Collection

```javascript
{
  _id: ObjectId,
  document_id: ObjectId,
  chunk_index: number,
  text: string,
  token_count: number,
  embedding_id: string,
  created_at: timestamp,
  metadata: {
    page_number: number,
    start_char: number,
    end_char: number
  }
}
```

### Search History Collection

```javascript
{
  _id: ObjectId,
  user_id: ObjectId,
  query: string,
  results_count: number,
  processing_time_ms: number,
  top_result_score: number,
  created_at: timestamp
}
```

---

## Services

### Vector DB Service

**Purpose**: Abstraction layer for vector databases

**Example Usage**:
```python
from app.services.vector_db_service import VectorDBService

# Create service (uses configured provider)
service = VectorDBService.create()

# Upsert vectors
await service.upsert_vectors([
    {
        "id": "chunk_1",
        "vector": [0.1, 0.2, 0.3, ...],  # embedding
        "metadata": {"document_id": "doc_1", "chunk_index": 0},
        "text": "Document text..."
    }
])

# Search
results = await service.search(
    query_vector=[0.1, 0.2, 0.3, ...],
    top_k=5
)
# Returns: [{"id": "...", "score": 0.95, "metadata": {...}}, ...]

# Get statistics
stats = await service.get_stats()
# Returns: {"total_vectors": 1000, "dimension": 384}
```

### Embeddings Service

**Purpose**: Generate text embeddings

**Example Usage**:
```python
from app.services.embeddings_service import EmbeddingsService

# Create service (uses configured provider)
embeddings = EmbeddingsService.create()

# Single embedding
vector = await embeddings.embed("Sample text to embed")
# Returns: [0.1, 0.2, 0.3, ...]

# Batch embeddings
vectors = await embeddings.embed_batch([
    "First text",
    "Second text",
    "Third text"
])
# Returns: [[0.1, ...], [0.2, ...], [0.3, ...]]

# Get embedding dimension
dim = embeddings.dimension  # 384 for MiniLM
```

### Redis Service

**Purpose**: Caching and session management

**Example Usage**:
```python
from app.services.redis_service import RedisService

# Create service (lazy initialization)
redis = RedisService.create()

# Set cache
await redis.set("key", "value", ttl=3600)

# Get cache
value = await redis.get("key")

# Delete
await redis.delete("key")

# Increment counter
count = await redis.increment("api_calls_user_123")
```

### Cloud Storage Service

**Purpose**: Multi-cloud file storage abstraction

**Example Usage**:
```python
from app.services.cloud_storage import CloudStorageService

# Create service (uses CLOUD_PROVIDER setting)
storage = CloudStorageService.create()

# Upload file
url = await storage.upload_file(
    file_path="document.pdf",
    key="documents/2025-11-30/doc.pdf"
)

# Download file
content = await storage.download_file("documents/2025-11-30/doc.pdf")

# Delete file
await storage.delete_file("documents/2025-11-30/doc.pdf")

# List files
files = await storage.list_files("documents/2025-11-30/")
```

---

## Background Tasks

### Celery Task Queue

**Purpose**: Handle long-running operations asynchronously

**Configured Tasks**:

```python
# Process uploaded document
@celery_app.task
def process_document_task(document_id, file_path):
    """
    1. Extract text from file
    2. Split into chunks
    3. Generate embeddings
    4. Index in vector DB
    5. Update document status
    """

# Generate embeddings for chunks
@celery_app.task
def generate_embeddings_task(document_id, chunks):
    """
    Generate embeddings for all document chunks
    """

# Index vectors in database
@celery_app.task
def index_vectors_task(document_id, vectors):
    """
    Store vectors in Chroma Cloud
    """

# Cleanup old data
@celery_app.task
def cleanup_old_data():
    """
    Remove old processed documents (daily)
    """
```

**Task Monitoring**:
```bash
# View task queue
celery -A app.tasks.celery_tasks inspect active

# View worker stats
celery -A app.tasks.celery_tasks inspect stats

# Flower monitoring UI
# Access: http://localhost:5555
```

---

## Security & Authentication

### JWT Authentication

**Token Lifecycle**:
```
1. User logs in → Generate JWT token
2. Client stores token in Authorization header
3. Every request validated against secret key
4. Token expires after configured time
5. Refresh token can extend session
```

**Token Claims**:
```python
{
    "sub": "user_id",           # Subject (user)
    "exp": 1234567890,         # Expiration time
    "iat": 1234567800,         # Issued at
    "username": "user@example.com",
    "scopes": ["read", "write"]
}
```

### Password Security

```python
# Bcrypt hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
hashed = pwd_context.hash("user_password")

# Verify password
is_valid = pwd_context.verify("user_password", hashed)
```

### Rate Limiting

**Configuration**:
```
- 60 API calls per minute (default)
- 5 file uploads per minute per user
- Sliding window rate limiting
```

**Exception Handling**:
```
HTTP 429 Too Many Requests
{
  "detail": "Rate limit exceeded. Try again later."
}
```

### CORS & Security Headers

**Middleware**:
- CORS (Cross-Origin Resource Sharing)
- HSTS (HTTP Strict Transport Security)
- CSP (Content Security Policy)
- X-Frame-Options (Clickjacking protection)

---

## Performance & Scaling

### Optimization Strategies

#### 1. **Caching Layer**
```
Redis cache for:
- User sessions (1 hour TTL)
- Search results (5 minute TTL)
- Document metadata (1 day TTL)
- Embedding vectors (7 day TTL)
```

#### 2. **Database Indexing**
```
MongoDB Indexes:
- username (unique)
- user_id (for fast queries)
- document_id (for chunks)
- created_at (for time-based queries)
- tags (for filtering)
```

#### 3. **Connection Pooling**
```
MongoDB:
- Pool size: 10 (default)
- Max overflow: 20
- Pre-ping enabled (health checks)

Redis:
- Connection pool for multiple workers
- Async client for non-blocking I/O
```

#### 4. **Async Processing**
```
FastAPI with async/await:
- Non-blocking I/O operations
- Concurrent request handling
- Background tasks via Celery

Celery workers:
- Configurable concurrency
- Process/thread pools
- Task retries with backoff
```

### Scaling Architecture

**Horizontal Scaling**:
```
Load Balancer (Nginx)
    │
    ├─► FastAPI Instance 1
    ├─► FastAPI Instance 2
    └─► FastAPI Instance 3

Shared Services:
    ├─► MongoDB (cloud)
    ├─► Redis Cloud
    ├─► Chroma Cloud
    └─► S3 Storage

Celery Workers (auto-scaled):
    ├─► Worker 1
    ├─► Worker 2
    └─► Worker N
```

**Load Testing**:
```bash
# Using Apache Bench
ab -n 1000 -c 10 http://localhost:8000/health

# Using wrk
wrk -t4 -c100 -d30s http://localhost:8000/health

# Using Locust
locust -f tests/load/locustfile.py
```

---

## Deployment

### Docker Deployment

**Single Service**:
```bash
# Build image
docker build -t doc-summ-agent:latest .

# Run container
docker run -d \
  -e MONGODB_URL=... \
  -e REDIS_CLOUD_ENDPOINT=... \
  -e GEMINI_API_KEY=... \
  -p 8000:8000 \
  doc-summ-agent:latest

# View logs
docker logs -f container_id
```

**Multi-Service (Docker Compose)**:
```bash
# Start all services
docker-compose up -d

# Scale workers
docker-compose up -d --scale celery-worker=3

# View logs
docker-compose logs -f api
```

### Kubernetes Deployment

**Helm Chart Installation**:
```bash
# (If a Helm chart exists)
helm install doc-summ-agent ./infra/helm-chart \
  --set mongodb.url=mongodb://... \
  --set redis.endpoint=redis://... \
  --set replicas=3
```

**Manual K8s Deployment**:
```bash
# Apply configurations
kubectl apply -f infra/k8s/

# Check deployment
kubectl get deployments
kubectl get pods
kubectl get services

# Scale replicas
kubectl scale deployment api --replicas=5

# View logs
kubectl logs -f deployment/api

# Rollback if needed
kubectl rollout undo deployment/api
```

### Environment-Specific Configurations

**Development**:
```env
DEBUG=true
ENVIRONMENT=development
LOG_LEVEL=DEBUG
MONGODB_URL=mongodb://localhost:27017/dev
REDIS_URL=redis://localhost:6379/0
```

**Production**:
```env
DEBUG=false
ENVIRONMENT=production
LOG_LEVEL=INFO
MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/
REDIS_URL=redis-cloud://endpoint:password
ENABLE_TRACING=true
```

---

## Troubleshooting

### Common Issues & Solutions

#### 1. **MongoDB Connection Error**

**Error**: `ServerSelectionTimeoutError`

**Solutions**:
```bash
# Check MongoDB URL format
# Should be: mongodb+srv://user:password@cluster.mongodb.net/?appName=app

# Test connection
python -c "from pymongo import MongoClient; MongoClient('your_url').admin.command('ping')"

# Check credentials in .env
grep MONGODB_URL .env
```

#### 2. **Redis Connection Error**

**Error**: `ConnectionError: Error 11002 connecting to...`

**Solutions**:
```bash
# Verify Redis Cloud credentials
echo "REDIS_CLOUD_ENDPOINT=..." >> .env
echo "REDIS_CLOUD_PASSWORD=..." >> .env

# Test Redis connection
redis-cli -h endpoint -p port -a password ping

# Check firewall/network
ping endpoint
```

#### 3. **Chroma Cloud Connection Error**

**Error**: `ValueError: illegal request line`

**Solutions**:
```bash
# Verify Chroma credentials
grep CHROMA .env

# Test credentials
python test_chroma_config.py

# Check API key validity (20+ chars)
# Verify tenant and database names
```

#### 4. **API Rate Limiting**

**Error**: `HTTP 429 Too Many Requests`

**Solutions**:
```python
# In .env
RATE_LIMIT_ENABLED=false  # Or increase limits

RATE_LIMIT_PER_MINUTE=120
RATE_LIMIT_UPLOAD_PER_MINUTE=10
```

#### 5. **Vector DB Not Indexed**

**Error**: Document indexed but search returns no results

**Solutions**:
```python
# Check if document was processed
# Verify vector_indexed field in MongoDB

# Re-index document
celery -A app.tasks.celery_tasks send_task(
    'app.tasks.celery_tasks.process_document_task',
    kwargs={'document_id': 'doc_id', ...}
)

# Check Chroma Cloud collection
python -c "
from app.services.vector_db_service import VectorDBService
service = VectorDBService.create()
print(service.collection.count())
"
```

#### 6. **Out of Memory Issues**

**Error**: MemoryError or OOMKilled

**Solutions**:
```bash
# Reduce batch size
CHUNK_SIZE=500  # default 1000

# Limit embeddings batch
EMBEDDING_BATCH_SIZE=32  # default 64

# Scale Celery workers
celery -A app.tasks.celery_tasks worker \
  --pool=prefork \
  --concurrency=2
```

#### 7. **Slow Search Performance**

**Error**: Search takes >5 seconds

**Solutions**:
```python
# Check Chroma index stats
stats = await vector_db.get_stats()
print(f"Total vectors: {stats['total_vectors']}")

# Reduce top_k parameter
# Default: 5, Try: 3

# Check Redis cache
redis_service = RedisService.create()
# Cache search results

# Add MongoDB indexes
db.documents.create_index("tags")
db.chunks.create_index("document_id")
```

#### 8. **Celery Task Failures**

**Error**: Tasks stuck in queue or failing silently

**Solutions**:
```bash
# View failed tasks
celery -A app.tasks.celery_tasks inspect active

# View task logs
celery -A app.tasks.celery_tasks events

# Flower monitoring
http://localhost:5555

# Retry failed tasks
celery -A app.tasks.celery_tasks purge  # Clear queue (careful!)
```

### Debug Mode

**Enable detailed logging**:
```env
LOG_LEVEL=DEBUG
LANGCHAIN_TRACING_V2=true
DEBUG=true
```

**Check logs**:
```bash
# Application logs
tail -f logs/app.log

# Docker logs
docker-compose logs -f api

# Kubernetes logs
kubectl logs -f deployment/api
```

**Health Check**:
```bash
curl -X GET http://localhost:8000/health

# Should return:
{
  "status": "healthy",
  "database": "connected",
  "redis": "connected",
  "vector_db": "connected"
}
```

---

## Advanced Topics

### Custom Embeddings Model

To use a different embeddings model:

```python
# In .env
EMBEDDING_PROVIDER=huggingface
HUGGINGFACE_MODEL_NAME=sentence-transformers/all-mpnet-base-v2
# Dimension will be 768 instead of 384
```

### Custom LLM Configuration

To use a different LLM:

```python
# In .env
LLM_PROVIDER=groq
GROQ_API_KEY=your_key
GROQ_MODEL=mixtral-8x7b-32768
```

### Vector Database Migration

To switch from local Chroma to Chroma Cloud:

```bash
# 1. Export local vectors
python scripts/export_vectors.py --from local --to backup.json

# 2. Update .env with Chroma Cloud credentials
CHROMA_API_KEY=...
CHROMA_TENANT=...
CHROMA_DATABASE=...

# 3. Import vectors to cloud
python scripts/import_vectors.py --from backup.json --to cloud
```

---

## Support & Resources

### Documentation Files
- `QUICK_START.md` - Quick start guide
- `PRODUCTION_STRUCTURE.md` - Complete structure
- `RAG_ENABLED.md` - RAG configuration
- `SETUP_GUIDE.md` - Detailed setup
- `MONGODB_SETUP.md` - MongoDB guide
- `REDIS_CLOUD_SETUP.md` - Redis Cloud guide
- `NO_DOCKER_SETUP.md` - Standalone setup

### GitHub
- Repository: https://github.com/Aka-Nine/Document-Summarizer-Agent
- Issues: https://github.com/Aka-Nine/Document-Summarizer-Agent/issues

### External Resources
- FastAPI Documentation: https://fastapi.tiangolo.com/
- MongoDB Docs: https://docs.mongodb.com/
- Chroma Docs: https://docs.trychroma.com/
- LangChain Docs: https://python.langchain.com/

---

## Conclusion

This Enterprise Document Intelligence Platform provides a complete, production-ready solution for document processing and semantic search. With RAG capabilities, multi-LLM support, and cloud-native architecture, it scales to handle enterprise workloads.

**Key Strengths**:
✅ Production-grade architecture
✅ Multi-provider support (LLM, Vector DB, Storage)
✅ Enterprise security and monitoring
✅ Cloud-native & scalable
✅ Comprehensive documentation
✅ Easy to customize and extend

**Next Steps**:
1. Complete environment configuration in `.env`
2. Start with `python run.py` for development
3. Scale using Docker or Kubernetes for production
4. Monitor with Flower and Prometheus
5. Extend with custom routes and logic

---

**Document Generated**: November 30, 2025  
**Version**: 2.0.0  
**Last Updated**: Current Session
