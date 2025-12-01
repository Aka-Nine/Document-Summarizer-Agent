# Enterprise Document Intelligence Platform

A production-ready document processing platform with RAG (Retrieval Augmented Generation) capabilities.

## 🔗 Repository

**GitHub**: [https://github.com/Aka-Nine/Document-Summarizer-Agent](https://github.com/Aka-Nine/Document-Summarizer-Agent)

## 🏗️ Project Structure

```
doc-summ-agent/
├── app/                    # Main application package
│   ├── api/               # API layer (FastAPI)
│   ├── core/              # Business logic
│   ├── models/            # Data models (MongoDB)
│   ├── services/          # External services
│   ├── middleware/        # Middleware
│   ├── tasks/             # Celery tasks
│   └── config/            # Configuration
│
├── tests/                 # Test suite
├── scripts/               # Utility scripts
├── infra/                 # Infrastructure configs
├── storage/               # File storage
├── chroma_db/             # Vector database
└── logs/                  # Application logs
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
python -m pip install "pymongo[srv]"
```

### 2. Configure Environment
Copy `.env.example` to `.env` and configure:
- MongoDB Atlas connection
- Redis Cloud connection
- Gemini API key
- Other service credentials

### 3. Run Application
```bash
# Start FastAPI server
python run.py

# Start Celery worker (separate terminal)
celery -A app.tasks.celery_tasks worker --loglevel=info
```

### 4. Access API
- API Docs: http://localhost:8000/docs
- Test Endpoint: http://localhost:8000/test

## ✨ Features

- ✅ **RAG Enabled** - Semantic search and retrieval
- ✅ **MongoDB** - Cloud database (Atlas)
- ✅ **Redis Cloud** - Task queue and caching
- ✅ **Gemini LLM** - Primary AI model
- ✅ **Filesystem Storage** - Local file storage (no Docker)
- ✅ **Chroma Vector DB** - Local vector storage
- ✅ **HuggingFace Embeddings** - Free embeddings

## 📚 Documentation

- `PRODUCTION_STRUCTURE.md` - Complete structure guide
- `RAG_ENABLED.md` - RAG configuration
- `SETUP_GUIDE.md` - Detailed setup instructions
- `QUICK_START.md` - Quick start guide

## 🎯 Production Ready

- ✅ Production-level structure
- ✅ Proper import organization
- ✅ Docker support
- ✅ Kubernetes configs
- ✅ Monitoring setup
- ✅ Logging infrastructure

---

**Built for Enterprise Document Intelligence** 🚀

