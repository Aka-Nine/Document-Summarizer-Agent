# Libraries and Dependencies

This document provides a comprehensive overview of all libraries used in the Document Summarization Agent project, organized by category and purpose.

## 📚 Core Application Libraries

### Web Framework & API
| Library | Version | Purpose | Used In |
|---------|---------|---------|---------|
| **fastapi** | 0.111.0 | Modern, fast web framework for building APIs | `api/main.py` |
| **uvicorn** | 0.30.6 | ASGI server for running FastAPI | `run.py` |
| **starlette** | 0.37.2 | Lightweight ASGI framework (FastAPI dependency) | Auto-included |
| **python-multipart** | 0.0.20 | Handle file uploads and form data | `api/main.py` |
| **slowapi** | 0.1.9 | Rate limiting for FastAPI | `api/main.py` |

### Database & ORM
| Library | Version | Purpose | Used In |
|---------|---------|---------|---------|
| **SQLAlchemy** | 2.0.41 | SQL toolkit and ORM | `models/database.py`, `api/main.py` |
| **psycopg2-binary** | 2.9.10 | PostgreSQL adapter for Python | Database connections |
| **alembic** | 1.16.3 | Database migration tool | (Available for migrations) |

### Authentication & Security
| Library | Version | Purpose | Used In |
|---------|---------|---------|---------|
| **python-jose** | 3.3.0 | JWT token encoding/decoding | `api/main.py` |
| **passlib** | 1.7.4 | Password hashing library | `api/main.py` |
| **bcrypt** | 4.3.0 | Password hashing algorithm | `api/main.py` |
| **cryptography** | 45.0.5 | Cryptographic primitives | Security operations |

### Background Tasks & Message Queue
| Library | Version | Purpose | Used In |
|---------|---------|---------|---------|
| **celery** | 5.5.3 | Distributed task queue | `tasks/celery_tasks.py` |
| **kombu** | 5.5.4 | Messaging library for Celery | Celery dependency |
| **billiard** | 4.2.1 | Multiprocessing pool for Celery | Celery dependency |
| **amqp** | 5.3.1 | AMQP protocol support | Celery dependency |
| **flower** | 2.0.1 | Celery monitoring tool | (Available for monitoring) |

### Caching & Storage
| Library | Version | Purpose | Used In |
|---------|---------|---------|---------|
| **redis** | 5.2.0 | Redis client for caching and message broker | `services/redis_service.py` |
| **minio** | 7.0.0 | MinIO client for object storage | `services/storage_service.py` |
| **boto3** | 1.39.4 | AWS SDK (MinIO compatibility) | MinIO dependency |
| **botocore** | 1.39.4 | Low-level AWS service client | Boto3 dependency |
| **s3transfer** | 0.13.0 | S3 transfer utilities | Boto3 dependency |

### AI/ML & Document Processing
| Library | Version | Purpose | Used In |
|---------|---------|---------|---------|
| **langchain** | 0.3.25 | Framework for LLM applications | `core/document_processor.py` |
| **langchain-core** | 0.3.64 | Core LangChain functionality | Document processing |
| **langchain-community** | 0.3.24 | Community integrations | `core/document_processor.py` |
| **langchain-groq** | 0.3.2 | Groq LLM integration | `core/document_processor.py` |
| **langchain-text-splitters** | 0.3.8 | Text splitting utilities | `core/document_processor.py` |
| **langgraph** | 0.4.8 | State machine for LLM workflows | `core/document_processor.py` |
| **langgraph-checkpoint** | 2.0.26 | Checkpointing for LangGraph | LangGraph dependency |
| **langgraph-prebuilt** | 0.2.2 | Prebuilt LangGraph components | LangGraph dependency |
| **langgraph-sdk** | 0.1.70 | SDK for LangGraph | LangGraph dependency |
| **langsmith** | 0.3.45 | LangChain observability | (Optional monitoring) |
| **groq** | 0.29.0 | Groq API client | LangChain-Groq dependency |
| **pypdf** | 5.6.1 | PDF processing library | Document loading |

### Data Validation & Serialization
| Library | Version | Purpose | Used In |
|---------|---------|---------|---------|
| **pydantic** | 2.11.7 | Data validation using Python type annotations | `api/main.py`, `config/setting.py` |
| **pydantic-settings** | 2.10.1 | Settings management with Pydantic | `config/setting.py` |
| **pydantic_core** | 2.33.2 | Core Pydantic functionality | Pydantic dependency |
| **marshmallow** | 3.26.1 | Object serialization/deserialization | Data validation |
| **dataclasses-json** | 0.6.7 | JSON serialization for dataclasses | Data handling |

### File Processing
| Library | Version | Purpose | Used In |
|---------|---------|---------|---------|
| **filetype** | 1.2.0 | File type detection | `api/main.py` |
| **pillow** | 11.3.0 | Image processing library | Image handling |
| **reportlab** | 4.4.2 | PDF generation | PDF operations |

### HTTP & Networking
| Library | Version | Purpose | Used In |
|---------|---------|---------|---------|
| **httpx** | 0.28.1 | Async HTTP client | HTTP requests |
| **httpx-sse** | 0.4.1 | Server-Sent Events for HTTPX | SSE support |
| **httpcore** | 1.0.9 | Core HTTP functionality | HTTPX dependency |
| **aiohttp** | 3.12.13 | Async HTTP client/server | Async operations |
| **requests** | 2.32.4 | HTTP library | HTTP requests |
| **urllib3** | 2.5.0 | HTTP client library | Requests dependency |
| **h11** | 0.16.0 | HTTP/1.1 protocol implementation | HTTPX dependency |
| **httptools** | 0.6.4 | Fast HTTP parser | Performance optimization |

### Logging & Monitoring
| Library | Version | Purpose | Used In |
|---------|---------|---------|---------|
| **structlog** | 25.4.0 | Structured logging | All modules |
| **prometheus_client** | 0.22.1 | Prometheus metrics client | (Available for metrics) |

### Configuration & Environment
| Library | Version | Purpose | Used In |
|---------|---------|---------|---------|
| **python-dotenv** | 1.0.1 | Load environment variables from .env | `config/setting.py` |
| **pydantic-settings** | 2.10.1 | Settings management | `config/setting.py` |

### Retry & Resilience
| Library | Version | Purpose | Used In |
|---------|---------|---------|---------|
| **tenacity** | 9.1.2 | Retry library with exponential backoff | `api/main.py` |

### Utilities & Helpers
| Library | Version | Purpose | Used In |
|---------|---------|---------|---------|
| **click** | 8.2.1 | Command-line interface creation | CLI tools |
| **typer** | 0.16.0 | Modern CLI framework | CLI tools |
| **rich** | 14.0.0 | Rich text and beautiful formatting | Terminal output |
| **python-dateutil** | 2.9.0.post0 | Date/time utilities | Date handling |
| **pytz** | 2025.2 | Timezone definitions | Timezone handling |
| **tzdata** | 2025.2 | Timezone database | Timezone support |
| **humanize** | 4.12.3 | Human-readable values | User-friendly output |

### JSON & Data Formats
| Library | Version | Purpose | Used In |
|---------|---------|---------|---------|
| **orjson** | 3.10.18 | Fast JSON library | JSON operations |
| **ujson** | 5.10.0 | Ultra-fast JSON encoder/decoder | JSON operations |
| **ormsgpack** | 1.10.0 | MessagePack serialization | Data serialization |
| **PyYAML** | 6.0.2 | YAML parser | Configuration files |

### Type Checking & Validation
| Library | Version | Purpose | Used In |
|---------|---------|---------|---------|
| **typing_extensions** | 4.14.1 | Backported typing features | Type hints |
| **typing-inspect** | 0.9.0 | Runtime inspection of types | Type checking |
| **typing-inspection** | 0.4.1 | Type inspection utilities | Type checking |
| **annotated-types** | 0.7.0 | Annotated type support | Type annotations |
| **mypy_extensions** | 1.1.0 | Extensions for mypy | Type checking |

### Email & Validation
| Library | Version | Purpose | Used In |
|---------|---------|---------|---------|
| **email-validator** | 2.1.0 | Email validation | `api/main.py` |

### Development & Testing
| Library | Version | Purpose | Used In |
|---------|---------|---------|---------|
| **watchfiles** | 1.1.0 | File watching for auto-reload | Development |
| **fastapi-cli** | 0.0.8 | FastAPI CLI tools | Development |

### Low-Level Dependencies
| Library | Version | Purpose |
|---------|---------|---------|
| **cffi** | 1.17.1 | C Foreign Function Interface |
| **greenlet** | 3.2.3 | Lightweight coroutines |
| **numpy** | 2.3.1 | Numerical computing |
| **certifi** | 2025.7.9 | SSL certificate bundle |
| **charset-normalizer** | 3.4.2 | Character encoding detection |
| **idna** | 3.10 | Internationalized Domain Names |
| **sniffio** | 1.3.1 | Async library detection |
| **anyio** | 4.9.0 | Async I/O compatibility |
| **aiohappyeyeballs** | 2.6.1 | Happy Eyeballs algorithm |
| **aiosignal** | 1.4.0 | Async signal handling |
| **frozenlist** | 1.7.0 | Immutable list implementation |
| **multidict** | 6.6.3 | Multi-value dictionary |
| **yarl** | 1.20.1 | URL parsing library |
| **attrs** | 25.3.0 | Classes without boilerplate |
| **packaging** | 24.2 | Core utilities for Python packages |
| **six** | 1.17.0 | Python 2/3 compatibility |
| **rsa** | 4.9.1 | RSA encryption |
| **ecdsa** | 0.19.1 | ECDSA cryptography |
| **pyasn1** | 0.6.1 | ASN.1 library |
| **pycparser** | 2.22 | C parser in Python |
| **wrapt** | 1.17.2 | Decorators and function wrappers |
| **propcache** | 0.3.2 | Property caching |
| **xxhash** | 3.5.0 | Extremely fast hash algorithm |
| **zstandard** | 0.23.0 | Zstandard compression |
| **limits** | 5.4.0 | Rate limiting utilities |
| **tornado** | 6.5.1 | Web framework (Flower dependency) |
| **websockets** | 15.0.1 | WebSocket implementation |
| **distro** | 1.9.0 | OS distribution detection |
| **dnspython** | 2.7.0 | DNS toolkit |
| **shellingham** | 1.5.4 | Shell detection |
| **colorama** | 0.4.6 | Cross-platform colored terminal text |
| **prompt_toolkit** | 3.0.51 | Interactive command-line tools |
| **wcwidth** | 0.2.13 | Wide character width |
| **Pygments** | 2.19.2 | Syntax highlighting |
| **Jinja2** | 3.1.6 | Template engine |
| **MarkupSafe** | 3.0.2 | Safe string handling |
| **Mako** | 1.3.10 | Template library |
| **markdown-it-py** | 3.0.0 | Markdown parser |
| **mdurl** | 0.1.2 | Markdown URL utilities |
| **jmespath** | 1.0.1 | JSON matching expressions |
| **jsonpatch** | 1.33 | JSON Patch implementation |
| **jsonpointer** | 3.0.0 | JSON Pointer implementation |
| **requests-toolbelt** | 1.0.0 | Utilities for requests library |
| **rich-toolkit** | 0.14.8 | Rich text toolkit |
| **click-didyoumean** | 0.3.1 | Did you mean for Click |
| **click-plugins** | 1.1.1.2 | Click plugins |
| **click-repl** | 0.3.0 | Click REPL |
| **Deprecated** | 1.2.18 | Deprecation warnings |
| **configparser** | 7.2.0 | Configuration file parser |
| **vine** | 5.1.0 | Promise-like library |

## 📦 Library Usage by Module

### `api/main.py`
- **fastapi** - Web framework
- **slowapi** - Rate limiting
- **sqlalchemy** - Database ORM
- **structlog** - Logging
- **python-jose** - JWT tokens
- **passlib** - Password hashing
- **pydantic** - Data validation
- **tenacity** - Retry logic
- **filetype** - File type detection

### `core/document_processor.py`
- **langchain** - LLM framework
- **langchain-groq** - Groq integration
- **langchain-community** - Document loaders
- **langgraph** - Workflow management
- **pypdf** - PDF processing
- **structlog** - Logging

### `services/storage_service.py`
- **minio** - Object storage client
- **structlog** - Logging

### `services/redis_service.py`
- **redis** - Redis client
- **structlog** - Logging

### `tasks/celery_tasks.py`
- **celery** - Task queue
- **sqlalchemy** - Database ORM
- **structlog** - Logging

### `models/database.py`
- **sqlalchemy** - Database ORM
- **psycopg2-binary** - PostgreSQL adapter

### `config/setting.py`
- **pydantic-settings** - Settings management
- **python-dotenv** - Environment variables

## 🎯 Key Library Categories

### Essential (Must Have)
1. **FastAPI** - Web framework
2. **SQLAlchemy** - Database ORM
3. **Celery** - Background tasks
4. **Redis** - Caching & message broker
5. **MinIO** - Object storage
6. **LangChain** - AI/ML framework
7. **Pydantic** - Data validation

### Important (Highly Recommended)
1. **python-jose** - Authentication
2. **passlib** - Password security
3. **structlog** - Logging
4. **tenacity** - Resilience
5. **slowapi** - Rate limiting

### Optional (Can Remove if Not Needed)
1. **flower** - Celery monitoring (can be removed)
2. **langsmith** - LangChain observability (optional)
3. **prometheus_client** - Metrics (if not using Prometheus)
4. **alembic** - Migrations (if not using migrations)

## 📊 Dependency Tree Summary

```
doc-summ-agent
├── FastAPI (Web Framework)
│   ├── Starlette
│   ├── Pydantic
│   └── Uvicorn
├── Celery (Task Queue)
│   ├── Kombu
│   ├── Redis
│   └── Billiard
├── LangChain (AI Framework)
│   ├── LangChain-Core
│   ├── LangChain-Community
│   ├── LangChain-Groq
│   └── LangGraph
├── SQLAlchemy (Database)
│   └── psycopg2-binary
├── MinIO (Storage)
│   └── boto3
└── Redis (Cache/Broker)
```

## 🔧 Total Library Count

- **Total Libraries**: 123
- **Direct Dependencies**: ~20
- **Transitive Dependencies**: ~103

## 💡 Recommendations

1. **Keep Core Libraries**: FastAPI, SQLAlchemy, Celery, Redis, MinIO, LangChain
2. **Consider Removing**: Flower (if not monitoring), LangSmith (if not using observability)
3. **Monitor Updates**: Regularly update security-critical libraries (cryptography, python-jose, passlib)
4. **Optimize**: Consider removing unused dependencies to reduce image size

---

*Last Updated: Based on current requirements.txt*

