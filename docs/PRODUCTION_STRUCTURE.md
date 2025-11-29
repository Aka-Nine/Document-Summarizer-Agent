# 🏗️ Production-Level Project Structure

## 📁 Directory Structure

```
doc-summ-agent/
├── app/                          # Main application package
│   ├── __init__.py
│   ├── api/                      # API layer
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application entry point
│   │   └── v1/                   # API version 1
│   │       ├── __init__.py
│   │       ├── routes.py        # SQL routes (legacy)
│   │       └── routes_mongodb.py # MongoDB routes (active)
│   ├── core/                     # Business logic
│   │   ├── __init__.py
│   │   ├── document_processor.py
│   │   ├── enterprise_document_processor.py
│   │   └── rag_processor.py
│   ├── models/                   # Data models
│   │   ├── __init__.py
│   │   ├── database.py          # SQL models (legacy)
│   │   └── mongodb_database.py   # MongoDB models (active)
│   ├── services/                 # External services
│   │   ├── __init__.py
│   │   ├── cloud_storage.py
│   │   ├── embeddings_service.py
│   │   ├── redis_service.py
│   │   ├── storage_service.py
│   │   └── vector_db_service.py
│   ├── middleware/               # Middleware
│   │   ├── __init__.py
│   │   └── production.py
│   ├── tasks/                    # Celery tasks
│   │   ├── __init__.py
│   │   └── celery_tasks.py
│   └── config/                   # Configuration
│       ├── __init__.py
│       ├── setting.py           # Legacy
│       └── settings.py          # Active
│
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── unit/                    # Unit tests
│   │   └── __init__.py
│   └── integration/             # Integration tests
│       └── __init__.py
│
├── scripts/                      # Utility scripts
│   └── setup.sh
│
├── infra/                        # Infrastructure configurations
│   ├── nginx/                    # Nginx configs
│   │   └── nginx.conf
│   ├── kubernetes/               # K8s manifests
│   ├── docker/                   # Docker configs
│   ├── k8s/                      # K8s resources
│   ├── monitoring/               # Monitoring configs
│   │   ├── prometheus.yml
│   │   └── grafana/
│   └── ssl/                      # SSL certificates
│
├── storage/                      # File storage (filesystem)
│   └── .gitkeep
│
├── chroma_db/                    # Vector database storage
│   └── .gitkeep
│
├── logs/                         # Application logs
│   └── .gitkeep
│
├── run.py                        # Application entry point
├── celery_worker.py              # Celery worker entry point
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker image definition
├── docker-compose.yml            # Docker Compose configuration
├── .env                          # Environment variables (not in git)
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore rules
└── README.md                     # Project documentation
```

---

## 🎯 Key Principles

### 1. **Separation of Concerns**
- `app/api/` - API endpoints and routing
- `app/core/` - Business logic and domain models
- `app/models/` - Data models and database schemas
- `app/services/` - External service integrations
- `app/middleware/` - Request/response middleware
- `app/tasks/` - Background task definitions

### 2. **Configuration Management**
- `app/config/` - Centralized configuration
- `.env` - Environment-specific variables (not in git)
- `.env.example` - Template for environment variables

### 3. **Infrastructure as Code**
- `infra/` - All infrastructure configurations
- `Dockerfile` - Container definition
- `docker-compose.yml` - Local development orchestration

### 4. **Testing Structure**
- `tests/unit/` - Unit tests
- `tests/integration/` - Integration tests

### 5. **Data Storage**
- `storage/` - User-uploaded files
- `chroma_db/` - Vector database files
- `logs/` - Application logs

---

## 📦 Import Structure

All imports use the `app.` prefix:

```python
# ✅ Correct
from app.config.settings import settings
from app.models.mongodb_database import get_database
from app.services.redis_service import RedisService
from app.core.enterprise_document_processor import EnterpriseDocumentProcessor
from app.tasks.celery_tasks import process_document_task

# ❌ Incorrect (old structure)
from config.settings import settings
from models.mongodb_database import get_database
```

---

## 🚀 Entry Points

### Application Server
```bash
python run.py
```
- Entry: `run.py`
- Imports: `app.api.main:app`

### Celery Worker
```bash
celery -A app.tasks.celery_tasks worker --loglevel=info
```
- Entry: `celery_worker.py`
- Imports: `app.tasks.celery_tasks`

---

## ✅ Benefits

1. **Clear Organization** - Easy to find and maintain code
2. **Scalability** - Easy to add new features and modules
3. **Testability** - Clear separation makes testing easier
4. **Production Ready** - Follows industry best practices
5. **Team Collaboration** - Clear structure for multiple developers

---

## 📝 Next Steps

1. ✅ Structure reorganized
2. ✅ Imports updated
3. ✅ Entry points updated
4. ⏭️ Add comprehensive tests
5. ⏭️ Add CI/CD configuration
6. ⏭️ Add monitoring and logging setup

---

**Your project is now organized for production!** 🎉

