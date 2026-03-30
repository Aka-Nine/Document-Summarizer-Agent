# 🤖 Document Summarizer Agent

> **An enterprise-grade AI system for intelligent document summarization and question answering, powered by Retrieval-Augmented Generation (RAG).**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Celery](https://img.shields.io/badge/Celery-Async-37814A?style=flat&logo=celery&logoColor=white)](https://docs.celeryq.dev)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=flat&logo=mongodb&logoColor=white)](https://mongodb.com)
[![Redis](https://img.shields.io/badge/Redis-Broker-DC382D?style=flat&logo=redis&logoColor=white)](https://redis.io)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker&logoColor=white)](https://docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture Diagram](#-architecture-diagram)
- [Features](#-features)
- [Tech Stack](#️-tech-stack)
- [Project Structure](#-project-structure)
- [Data Flow](#-data-flow)
- [API Endpoints](#-api-endpoints)
- [Database Schema](#-database-schema)
- [Security Architecture](#-security-architecture)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [Running with Docker](#-running-with-docker)
- [Running Locally](#-running-locally)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Performance](#-performance)
- [Known Limitations](#-known-limitations)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)

---

## 🧠 Overview

The **Document Summarizer Agent** is a production-ready, end-to-end AI platform that allows users to upload documents, extract semantic meaning, and query them using natural language. Built on a **Retrieval-Augmented Generation (RAG)** pipeline, it leverages state-of-the-art vector embeddings and large language models to deliver grounded, context-aware summaries and answers.

The platform is designed with **scalability**, **modularity**, and **production readiness** in mind — featuring async task processing, multi-cloud integrations, a secure REST API with JWT authentication, and a full observability stack.

**What can it do?**

- Upload PDF, DOCX, and TXT documents via a REST API or frontend UI
- Asynchronously extract, chunk, and embed document content
- Generate document-level summaries using Gemini LLM
- Answer natural language questions grounded in document content (RAG)
- Retrieve past summaries and query history via authenticated APIs
- Monitor system health across all connected services

---

## 🏛️ Architecture Diagram

![System Architecture]()
> The system is organized into four horizontal layers: **Client**, **API Layer**, **Async Workers**, and **Data Layer**. Each layer communicates through well-defined interfaces, enabling independent scaling and testing.

### Layer Breakdown

**Client Layer** — React/TypeScript frontend, REST clients (cURL/Postman), and Swagger UI at `/docs`.

**API Layer** — FastAPI application with a 7-layer middleware stack (JWT Auth, Rate Limiting, CORS, Security Headers, GZip, Request ID tracing, Structured Logging). Routes are versioned under `/api/v1/`.

**Async Workers Layer** — Celery workers consume tasks from a Redis message broker. The document processing pipeline runs entirely asynchronously: text extraction → chunking → embedding generation → LLM summarization. The RAG pipeline also runs here at query time.

**Data Layer** — Three storage systems: MongoDB Atlas (metadata, user accounts, summaries), Chroma DB (384-dimensional vector embeddings for semantic search), and local filesystem storage (raw uploaded documents).

---

## ✨ Features

- **RAG-based Q&A** — Semantic vector search retrieves top-K chunks before sending context to the LLM, grounding answers in document facts
- **Async Document Processing** — Celery + Redis ensures the API stays responsive while processing runs in the background
- **Multi-format Support** — Ingests PDF, DOCX, and TXT files with automatic content extraction
- **JWT Authentication** — All protected endpoints require a valid Bearer token; bcrypt password hashing for user credentials
- **Rate Limiting** — SlowAPI middleware enforces per-IP rate limits, returning 429 on breach
- **Structured Logging** — Every request gets a UUID; logs are emitted in JSON with full request context
- **Security Headers** — 7 HTTP security headers applied on every response (HSTS, CSP, X-Frame-Options, etc.)
- **Health Checks** — `/health` endpoint verifies connectivity to MongoDB, Redis, Chroma, and filesystem
- **LangSmith Tracing** — Optional LLM call tracing and observability
- **Dockerized** — Full `docker-compose.dev.yml` for one-command local setup
- **CI/CD** — GitHub Actions workflow for linting, testing, and deployment
- **Render Deployment** — `render.yaml` config for cloud deployment out of the box

---

## 🛠️ Tech Stack

### Backend

| Technology | Role |
|---|---|
| **Python 3.10+** | Core language |
| **FastAPI** | Async REST API framework |
| **Pydantic** | Request/response validation and settings management |
| **Celery** | Distributed async task queue |
| **Redis** | Celery message broker + session/cache store |
| **Uvicorn** | ASGI server |
| **SlowAPI** | Rate limiting middleware |
| **python-jose** | JWT token generation and validation |
| **passlib + bcrypt** | Password hashing |
| **structlog** | Structured JSON logging |

### AI / ML

| Technology | Role |
|---|---|
| **Google Gemini** | LLM for summarization and Q&A generation |
| **HuggingFace `all-MiniLM-L6-v2`** | Sentence embedding model (384-dim vectors) |
| **LangChain** | RAG pipeline orchestration |
| **LangSmith** | LLM call tracing and observability |
| **Chroma DB** | Vector database for semantic similarity search |

### Document Processing

| Technology | Role |
|---|---|
| **PyMuPDF / pdfplumber** | PDF text extraction |
| **docx2txt / python-docx** | DOCX text extraction |
| **LangChain TextSplitter** | Semantic document chunking |

### Storage & Database

| Technology | Role |
|---|---|
| **MongoDB Atlas** | User accounts, document metadata, query history |
| **Chroma DB** | Vector embeddings (cloud or local persistence) |
| **Local Filesystem** | Raw uploaded document files (`storage/`) |

### DevOps & Infrastructure

| Technology | Role |
|---|---|
| **Docker & Docker Compose** | Containerized development environment |
| **GitHub Actions** | CI/CD pipeline (lint, test, deploy) |
| **Render** | Cloud deployment target (`render.yaml`) |
| **Terraform (HCL)** | Infrastructure-as-code (`infra/`) |
| **Pre-commit** | Git hooks for code quality enforcement |

---

## 📁 Project Structure

```
Document-Summarizer-Agent/
│
├── api/                        # FastAPI route definitions
│   ├── v1/
│   │   ├── auth.py             # /auth/register, /auth/login
│   │   ├── documents.py        # /documents/upload, /documents/{id}
│   │   ├── query.py            # /documents/{id}/query
│   │   ├── search.py           # /search
│   │   └── analytics.py        # /analytics
│
├── app/                        # Core application logic
│   ├── main.py                 # FastAPI app init, middleware registration
│   ├── dependencies.py         # FastAPI Depends() injectors
│   └── middleware/             # Custom middleware (logging, rate limit, etc.)
│
├── tasks/                      # Celery background tasks
│   ├── worker.py               # Celery app definition
│   ├── document_tasks.py       # Text extract, chunk, embed, summarize
│   └── embedding_tasks.py      # Vector generation tasks
│
├── models/                     # Pydantic & MongoDB models
│   ├── user.py                 # User schema
│   ├── document.py             # Document schema
│   └── query.py                # Query/response schema
│
├── config/                     # Configuration management
│   ├── settings.py             # Pydantic settings (reads .env)
│   └── .env.example            # Environment variable template
│
├── chroma_db/                  # Chroma vector DB local storage/config
│
├── frontend/                   # React + TypeScript UI
│   ├── src/
│   │   ├── components/         # UI components
│   │   ├── pages/              # Page views
│   │   └── api/                # API client calls
│   ├── package.json
│   └── tsconfig.json
│
├── storage/                    # Uploaded document files (raw)
│
├── infra/                      # Terraform infrastructure configs
│
├── scripts/                    # Utility scripts (health checks, migrations)
│
├── tests/                      # Automated test suite
│   ├── test_api.py             # API route tests
│   └── local_test_client.py    # In-process FastAPI TestClient
│
├── docs/                       # Extended documentation
│   ├── API_TESTING_WITH_CURL.sh
│   ├── API_Testing_PowerShell.ps1
│   └── Postman_Collection.json
│
├── .github/workflows/          # GitHub Actions CI/CD
├── docker-compose.dev.yml      # Development Docker Compose
├── render.yaml                 # Render deployment config
├── .pre-commit-config.yaml     # Pre-commit hooks
└── run.py                      # Application entry point
```

---

## 🔄 Data Flow

### 1. Document Upload Flow

```
User (POST /api/v1/documents/upload)
    │
    ├─▶ [JWT Auth Middleware] — validate Bearer token
    ├─▶ [Rate Limit Middleware] — check request quota
    ├─▶ File Validation — check MIME type (PDF/DOCX/TXT)
    ├─▶ Save file → storage/ directory
    ├─▶ Create document record in MongoDB (status: "processing")
    ├─▶ Dispatch Celery task (document_id)
    └─▶ Return 202 Accepted + document_id

Celery Worker picks up task:
    ├─▶ Extract raw text (PyMuPDF / docx2txt)
    ├─▶ Clean & normalize text
    ├─▶ Split into semantic chunks (LangChain TextSplitter)
    ├─▶ Generate 384-dim embeddings per chunk (HuggingFace)
    ├─▶ Upsert vectors into Chroma DB
    ├─▶ Send chunks to Gemini LLM → generate summary
    └─▶ Update MongoDB document record (status: "ready", summary saved)
```

### 2. RAG Query Flow

```
User (POST /api/v1/documents/{id}/query)
    │  Body: { "question": "What are the key findings?" }
    │
    ├─▶ [Auth + Rate Limit Middleware]
    ├─▶ Embed the user question (HuggingFace)
    ├─▶ Run semantic similarity search in Chroma DB
    ├─▶ Retrieve Top-K relevant chunks
    ├─▶ Assemble context window from chunks
    ├─▶ Construct prompt: context + question → Gemini LLM
    ├─▶ Receive LLM-generated answer
    ├─▶ Save query + answer to MongoDB (queries collection)
    └─▶ Return 200 OK + { answer, sources }
```

### 3. Authentication Flow

```
User (POST /api/v1/auth/register)
    ├─▶ Validate email uniqueness in MongoDB
    ├─▶ Hash password with bcrypt
    └─▶ Create user document → return user_id

User (POST /api/v1/auth/login)
    ├─▶ Lookup user by email in MongoDB
    ├─▶ Verify password hash
    ├─▶ Generate JWT (signed, with expiry)
    └─▶ Return access_token

Protected requests:
    ├─▶ Extract Bearer token from Authorization header
    ├─▶ Verify JWT signature + expiry
    └─▶ Populate request context with user_id
```

---

## 🔌 API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/api/v1/auth/register` | ❌ | Register a new user |
| `POST` | `/api/v1/auth/login` | ❌ | Login and receive JWT |
| `POST` | `/api/v1/documents/upload` | ✅ | Upload a document for processing |
| `GET` | `/api/v1/documents` | ✅ | List all user documents |
| `GET` | `/api/v1/documents/{id}` | ✅ | Get document metadata |
| `GET` | `/api/v1/documents/{id}/summary` | ✅ | Retrieve generated summary |
| `POST` | `/api/v1/documents/{id}/query` | ✅ | Ask a question (RAG) |
| `GET` | `/api/v1/documents/{id}/queries` | ✅ | Get query history for document |
| `DELETE` | `/api/v1/documents/{id}` | ✅ | Delete document and vectors |
| `GET` | `/api/v1/search` | ✅ | Semantic search across documents |
| `GET` | `/api/v1/analytics` | ✅ | Usage analytics |
| `GET` | `/health` | ❌ | System health check (all services) |
| `GET` | `/docs` | ❌ | Swagger interactive API docs |
| `GET` | `/redoc` | ❌ | ReDoc API reference |

---

## 🗄️ Database Schema

### MongoDB — `users` collection

```json
{
  "_id": "ObjectId",
  "email": "string (unique)",
  "hashed_password": "string (bcrypt)",
  "full_name": "string",
  "created_at": "datetime",
  "updated_at": "datetime",
  "is_active": "boolean"
}
```

### MongoDB — `documents` collection

```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId (ref: users)",
  "filename": "string",
  "content_type": "string",
  "file_path": "string",
  "text_content": "string",
  "summary": "string",
  "chunk_count": "integer",
  "status": "processing | ready | failed",
  "created_at": "datetime",
  "metadata": {
    "page_count": "integer",
    "word_count": "integer",
    "language": "string"
  }
}
```

### MongoDB — `queries` collection

```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId (ref: users)",
  "document_id": "ObjectId (ref: documents)",
  "question": "string",
  "answer": "string",
  "context_chunks": ["string"],
  "model_used": "string",
  "created_at": "datetime",
  "response_time_ms": "integer",
  "tokens_used": "integer"
}
```

### Chroma DB — `document-intelligence` collection

```
ids:        [string]          → chunk-level unique identifiers
embeddings: [[float x 384]]   → HuggingFace all-MiniLM-L6-v2 vectors
documents:  [string]          → raw chunk text
metadatas:  [{
  document_id:  string,
  chunk_index:  integer,
  source:       string
}]
```

---

## 🔐 Security Architecture

The platform applies security at every layer:

**Authentication** — JWT-based Bearer tokens required on all `/api/v1/*` routes. Tokens carry expiry and are validated on every request by the `HTTPBearer` middleware.

**Password Security** — Passwords are hashed with bcrypt before storage. Raw passwords are never persisted.

**Rate Limiting** — SlowAPI enforces per-IP request limits. Requests exceeding the threshold receive HTTP 429.

**HTTP Security Headers** — Applied globally on every response:

```
X-Content-Type-Options:        nosniff
X-Frame-Options:               SAMEORIGIN
X-XSS-Protection:              1; mode=block
Strict-Transport-Security:     max-age=31536000; includeSubDomains
Content-Security-Policy:       default-src 'self'; script-src 'self' 'unsafe-inline'
Referrer-Policy:               strict-origin-when-cross-origin
Permissions-Policy:            geolocation=(), microphone=(), camera=()
```

**CORS** — Configurable allowed origins. Credentials are supported for frontend integration.

**Input Validation** — All request bodies are validated via Pydantic models before any processing begins.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Docker & Docker Compose
- Node.js 18+ (for frontend)
- A MongoDB Atlas account (or local MongoDB)
- A Redis instance (local, Docker, or Redis Cloud)
- A Google Gemini API key
- A Chroma DB account (or local Chroma)

---

## ⚙️ Environment Variables

Create a `.env` file in the `config/` directory. Use `config/.env.example` as a template:

```env
# Application
APP_ENV=development
SECRET_KEY=your-very-secret-jwt-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=60

# MongoDB
MONGO_URI=mongodb+srv://<user>:<password>@cluster.mongodb.net/
MONGO_DB_NAME=document_summarizer

# Redis
REDIS_URL=redis://localhost:6379/0

# Chroma DB
CHROMA_PERSIST_PATH=./chroma_db
# For Chroma Cloud:
# CHROMA_API_KEY=ck-xxxx
# CHROMA_TENANT=your-tenant
# CHROMA_DATABASE=your-database

# LLM (Google Gemini)
LLM_PROVIDER=gemini
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-pro

# Embeddings
EMBEDDING_MODEL=all-MiniLM-L6-v2

# LangSmith (optional observability)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-key
LANGCHAIN_PROJECT=document-summarizer-agent

# Storage
UPLOAD_DIR=./storage
MAX_FILE_SIZE_MB=50
```

---

## 🐳 Running with Docker

The fastest way to get the full stack running locally:

```bash
# 1. Clone the repository
git clone https://github.com/Aka-Nine/Document-Summarizer-Agent.git
cd Document-Summarizer-Agent

# 2. Set up environment variables
cp config/.env.example config/.env
# Edit config/.env with your API keys

# 3. Build and start all services
docker-compose -f docker-compose.dev.yml up --build

# Services started:
# - FastAPI API         → http://localhost:8000
# - Swagger UI          → http://localhost:8000/docs
# - Redis               → localhost:6379
# - Celery Worker       → background process
```

To run in detached mode:

```bash
docker-compose -f docker-compose.dev.yml up --build -d
```

To view logs:

```bash
docker-compose -f docker-compose.dev.yml logs -f
```

---

## 💻 Running Locally (Without Docker)

### Step 1 — Install Python dependencies

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2 — Start Redis

```bash
# macOS
brew install redis && brew services start redis

# Ubuntu/Debian
sudo apt install redis-server && sudo service redis start

# Windows — use WSL or Docker:
docker run -d -p 6379:6379 redis:alpine
```

### Step 3 — Start MongoDB

Either use MongoDB Atlas (set `MONGO_URI` in `.env`) or run locally:

```bash
docker run -d -p 27017:27017 mongo:6
```

### Step 4 — Start the Celery Worker

```bash
# Linux / macOS
celery -A tasks.worker worker --loglevel=info

# Windows (use solo pool to avoid multiprocessing issues)
celery -A tasks.worker worker --loglevel=info --pool=solo
```

### Step 5 — Start the FastAPI Server

```bash
python run.py
# API available at: http://localhost:8000
# Swagger UI at:    http://localhost:8000/docs
```

### Step 6 — (Optional) Start the Frontend

```bash
cd frontend
npm install
npm run dev
# Frontend at: http://localhost:3000
```

---

## 🧪 Testing

The project includes five testing approaches:

### 1. Python Test Suite

```bash
pytest tests/test_api.py -v
```

Covers: user registration, login, document upload, document retrieval, RAG queries, query history, auth errors, rate limiting, and health checks.

### 2. FastAPI TestClient (in-process, fastest)

```bash
python tests/local_test_client.py
```

### 3. cURL Examples

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secret", "full_name": "Jane Doe"}'

# Login and capture token
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secret"}' | jq -r '.access_token')

# Upload a document
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/path/to/your/document.pdf"

# Query a document
curl -X POST http://localhost:8000/api/v1/documents/{document_id}/query \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main conclusion of this document?"}'
```

More examples in `docs/API_TESTING_WITH_CURL.sh`.

### 4. PowerShell (Windows)

```powershell
# Run the provided test script
.\docs\API_Testing_PowerShell.ps1
```

### 5. Postman Collection

Import `docs/Postman_Collection.json` directly into Postman for a complete, ready-to-use API collection with environment variable support.

---

## ☁️ Deployment

### Render (Recommended)

The repository includes a `render.yaml` for one-click deployment:

```bash
# Push to GitHub, then connect repo in Render dashboard
# render.yaml handles service definitions automatically
```

### Manual Deployment Checklist

- [ ] Set all environment variables in production secrets manager
- [ ] Use MongoDB Atlas (not local) for production
- [ ] Use Redis Cloud for production broker/cache
- [ ] Use Chroma Cloud or a managed vector DB
- [ ] Set up SSL/TLS via a reverse proxy (Nginx/Caddy)
- [ ] Configure `ALLOWED_HOSTS` and `CORS_ORIGINS` for production domains
- [ ] Set `APP_ENV=production` to disable debug features
- [ ] Enable LangSmith tracing for LLM observability
- [ ] Set up uptime monitoring on `/health` endpoint

---

## 📈 Performance

| Operation | Typical Response Time |
|---|---|
| Health check | < 10 ms |
| User login | 50 – 100 ms |
| Document list | 100 – 200 ms |
| Vector similarity search | 200 – 500 ms |
| RAG query (end-to-end) | 2 – 5 seconds |
| Document processing (async) | 5 – 30 seconds (background) |

The API itself never blocks on document processing — Celery handles that asynchronously. The `/health` endpoint confirms readiness of all backing services.

---

## ⚠️ Known Limitations

- Large documents (100+ pages) significantly increase Celery processing time
- LLM token costs scale with document size; long documents consume more Gemini quota
- Chroma DB in local mode does not support horizontal scaling (use Chroma Cloud for multi-instance deployments)
- Current deployment is single-node; add a load balancer + multiple Uvicorn workers for high traffic
- No streaming responses yet — the LLM response is returned all at once

---

## 🔮 Roadmap

- [ ] **Streaming Summaries** — Stream LLM responses token-by-token via SSE
- [ ] **Multi-document Querying** — RAG across a corpus of documents simultaneously
- [ ] **User Authentication Tiers** — Free / Pro usage quotas
- [ ] **Cloud Vector DB Support** — Pinecone, Weaviate, Qdrant adapters
- [ ] **Improved Frontend UX** — Upload progress, real-time processing status
- [ ] **Query Caching** — Redis-based response cache for frequently asked questions
- [ ] **Batch Upload** — Process multiple documents in a single request
- [ ] **Export** — Download summaries as PDF or DOCX
- [ ] **Webhook Notifications** — Notify clients when async processing completes

---

## 🤝 Contributing

Contributions are welcome! To get started:

```bash
# 1. Fork the repo and clone your fork
git clone https://github.com/<your-username>/Document-Summarizer-Agent.git

# 2. Create a feature branch
git checkout -b feature/your-feature-name

# 3. Install pre-commit hooks
pip install pre-commit
pre-commit install

# 4. Make your changes and run tests
pytest tests/ -v

# 5. Commit and push
git commit -m "feat: describe your change"
git push origin feature/your-feature-name

# 6. Open a Pull Request
```

Please ensure your code passes linting (`pre-commit run --all-files`) and all tests pass before opening a PR.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/) — the async API framework that powers the backend
- [LangChain](https://python.langchain.com/) — RAG pipeline orchestration
- [Chroma DB](https://www.trychroma.com/) — fast, developer-friendly vector database
- [HuggingFace](https://huggingface.co/) — `all-MiniLM-L6-v2` embedding model
- [Google Gemini](https://deepmind.google/technologies/gemini/) — LLM powering summaries and Q&A
- [MongoDB Atlas](https://www.mongodb.com/atlas) — managed database layer
- [Celery](https://docs.celeryq.dev/) — distributed task queue

---

<div align="center">

**Built with ❤️ — combining async systems, vector search, LLM orchestration, and scalable backend architecture.**

[⭐ Star this repo](https://github.com/Aka-Nine/Document-Summarizer-Agent) · [🐛 Report a bug](https://github.com/Aka-Nine/Document-Summarizer-Agent/issues) · [💡 Request a feature](https://github.com/Aka-Nine/Document-Summarizer-Agent/issues)

</div>
