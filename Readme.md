# Document Processing API - Technology Stack Guide

## What This System Does

This is a document processing platform that takes PDF files uploaded by users and uses artificial intelligence to automatically create summaries and answer questions about the content. Think of it as having an AI assistant that can quickly read through long documents and extract the most important information for you.

---
##Flow Diagram
<img width="996" height="1272" alt="Document Processing System Architecture" src="https://github.com/user-attachments/assets/bb3ec2e9-2954-4cb0-96f7-d6fcc7780539" />

## The Technology Stack Explained

### FastAPI - The Web Framework

**What it is:** FastAPI is a modern Python web framework for building APIs (Application Programming Interfaces).

**Why we chose it:**
- **Speed**: One of the fastest Python frameworks available
- **Automatic Documentation**: Creates interactive API docs automatically
- **Type Safety**: Catches errors before they happen in production
- **Easy to Learn**: Simple syntax that's easy for developers to understand
- **Async Support**: Can handle many requests at the same time without blocking

**How it works in our system:**
FastAPI acts as the "front door" of our application. When users want to upload a document, check processing status, or retrieve results, they send requests to FastAPI. It handles user authentication, validates the data they send, and routes requests to the appropriate parts of our system.

**Real-world analogy:** Think of FastAPI as a receptionist at a busy office who greets visitors, checks their appointments, and directs them to the right department.

---

### PostgreSQL - The Main Database

**What it is:** PostgreSQL is a powerful, open-source relational database system.

**Why we chose it:**
- **Reliability**: Has been battle-tested for decades in production systems
- **ACID Compliance**: Ensures data consistency even during system failures
- **Rich Features**: Supports complex queries, JSON data, and advanced indexing
- **Scalability**: Can handle millions of records efficiently
- **Open Source**: No licensing costs and strong community support

**How it works in our system:**
PostgreSQL stores all the important information about users, documents, and processing results. When a user uploads a document, we store metadata like filename, upload time, and processing status. After AI processing completes, we store the summary and question-answer results here.

**Real-world analogy:** PostgreSQL is like a highly organized filing cabinet system where every piece of information has its proper place and can be quickly retrieved when needed.

---

### MinIO - Object Storage

**What it is:** MinIO is a high-performance object storage system that's compatible with Amazon S3.

**Why we chose it:**
- **S3 Compatible**: Works with existing S3 tools and libraries
- **Self-Hosted**: We control our own data instead of relying on external cloud providers
- **High Performance**: Optimized for large file operations
- **Scalable**: Can grow from single server to distributed clusters
- **Cost Effective**: No per-request charges like cloud storage

**How it works in our system:**
MinIO stores the actual PDF files that users upload. When someone uploads a document, we save it to MinIO with a unique identifier. Later, when our AI processing workers need to analyze the document, they download it from MinIO. We also use MinIO to store any processed files or generated reports.

**Real-world analogy:** MinIO is like a warehouse where we store all the physical documents, with a smart inventory system that can quickly locate and retrieve any file we need.

---

### Redis - Caching and Message Broker

**What it is:** Redis is an in-memory data structure store used as a cache and message broker.

**Why we chose it:**
- **Lightning Fast**: Stores data in memory for microsecond response times
- **Versatile**: Can be used for caching, queues, and real-time messaging
- **Persistent**: Can save data to disk for recovery after restarts
- **Scalable**: Supports clustering and replication
- **Simple**: Easy to set up and manage

**How it works in our system:**
Redis serves two main purposes:
1. **Task Queue**: When a document needs processing, we add a task to Redis queue
2. **Caching**: We store frequently accessed data in Redis for faster retrieval

**Real-world analogy:** Redis is like having a super-fast assistant who can instantly remember information you've asked for before, and also manages a to-do list that workers can pick tasks from.

---

### Celery - Background Task Processing

**What it is:** Celery is a distributed task queue system for Python.

**Why we chose it:**
- **Asynchronous**: Handles time-consuming tasks without blocking the main application
- **Distributed**: Can run workers on multiple machines
- **Reliable**: Ensures tasks are completed even if workers crash
- **Scalable**: Easy to add more workers when processing load increases
- **Monitoring**: Provides tools to track task progress and performance

**How it works in our system:**
When a user uploads a document, we don't process it immediately because AI analysis can take several minutes. Instead, we add a processing task to the Celery queue. Celery workers (separate processes) pick up these tasks and handle the heavy AI processing in the background while the user can continue using the application.

**Real-world analogy:** Celery is like having a team of specialized workers in a back room who handle complex tasks while the front desk continues serving customers without interruption.

---

### LangChain - AI Processing Framework

**What it is:** LangChain is a framework for building applications with large language models (LLMs).

**Why we chose it:**
- **Abstracts Complexity**: Simplifies working with different AI models
- **Chain Operations**: Allows combining multiple AI operations in sequence
- **Document Processing**: Built-in tools for handling text documents
- **Flexible**: Can work with various AI providers and models
- **Active Development**: Rapidly evolving with new features

**How it works in our system:**
LangChain orchestrates our AI processing pipeline. It takes a PDF document, extracts the text, splits it into manageable chunks, sends these chunks to the AI model for analysis, and then combines the results into a coherent summary and answers to questions.

**Real-world analogy:** LangChain is like a skilled translator who not only converts languages but also understands context, breaks down complex documents into understandable parts, and presents information in exactly the format you need.

---

### Groq/LLama3 - AI Language Model

**What it is:** Groq is a high-performance AI inference platform, and LLama3 is a state-of-the-art language model.

**Why we chose it:**
- **High Performance**: Groq hardware provides extremely fast AI inference
- **Cost Effective**: More affordable than many other AI services
- **Quality Results**: LLama3 produces high-quality summaries and answers
- **Reliable**: Consistent performance and uptime
- **API Integration**: Easy to integrate with our existing systems

**How it works in our system:**
When we need to analyze a document, we send the text to Groq's platform running LLama3. The AI model reads through the content and generates intelligent summaries and answers to questions. This is the "brain" of our system that actually understands and interprets the document content.

**Real-world analogy:** Groq/LLama3 is like having a brilliant research assistant who can quickly read through any document and provide insightful summaries and answer specific questions about the content.

---

## How All These Technologies Work Together

### The Complete Workflow

1. **User Interaction (FastAPI)**
   - User uploads a PDF through the web interface
   - FastAPI validates the file and user authentication
   - File gets stored in MinIO, metadata goes to PostgreSQL

2. **Task Queuing (Redis + Celery)**
   - A processing task is added to the Redis queue
   - FastAPI immediately responds to user that upload was successful
   - Celery worker picks up the task from the queue

3. **AI Processing (LangChain + Groq)**
   - Worker downloads the PDF from MinIO
   - LangChain extracts and processes the text
   - Groq/LLama3 generates summary and answers
   - Results are saved back to PostgreSQL

4. **Result Delivery (FastAPI + PostgreSQL)**
   - User can check processing status through API
   - Once complete, user retrieves summary and answers
   - Redis caches frequently accessed results for faster delivery

### Why This Architecture Works

**Scalability:** Each component can be scaled independently. Need more AI processing power? Add more Celery workers. Getting too many API requests? Add more FastAPI servers.

**Reliability:** If one component fails, others continue working. Failed tasks can be retried automatically.

**Performance:** Background processing means users don't wait for AI analysis. Caching ensures fast response times.

**Maintainability:** Each technology has a specific role, making the system easier to debug and update.

---

## Benefits of This Technology Stack

### For Users
- **Fast Uploads**: Documents are accepted immediately
- **Reliable Processing**: Tasks complete even during high load
- **Quick Access**: Results are cached for instant retrieval
- **Scalable**: System grows with user demand

### For Developers
- **Modern Tools**: Latest technologies with good documentation
- **Separation of Concerns**: Each component has a clear responsibility
- **Easy Testing**: Components can be tested independently
- **Good Documentation**: All technologies have strong community support

### For Business
- **Cost Effective**: Open-source technologies reduce licensing costs
- **Scalable**: Can handle growth without major architecture changes
- **Reliable**: Proven technologies with good track records
- **Flexible**: Easy to swap components or add new features

---

## Technology Alternatives and Why We Didn't Choose Them

### Instead of FastAPI, we could have used:
- **Flask**: Simpler but less performant and lacks automatic documentation
- **Django**: More features but heavier and overkill for an API-only service
- **Express.js**: Would require using JavaScript instead of Python

### Instead of PostgreSQL, we could have used:
- **MySQL**: Less advanced features for complex queries
- **MongoDB**: NoSQL would complicate relational data like user-document relationships
- **SQLite**: Not suitable for production-scale concurrent access

### Instead of MinIO, we could have used:
- **Amazon S3**: More expensive and creates cloud vendor lock-in
- **Local File System**: Doesn't scale across multiple servers
- **Google Cloud Storage**: Again, vendor lock-in and ongoing costs

### Instead of Redis, we could have used:
- **RabbitMQ**: More complex setup and management
- **Apache Kafka**: Overkill for our message volume
- **Database Queue**: Would slow down our main database

This technology stack gives us the best balance of performance, reliability, cost-effectiveness, and ease of development for our specific use case of AI-powered document processing.

---

## Project Structure & Setup Guide

### 📁 Project Structure

```
document-processing-api/
├── main.py                    # FastAPI entrypoint - handles all HTTP requests
├── celery_tasks.py           # Celery background tasks - processes documents
├── document_processor.py     # Core LLM processing - AI analysis logic
├── database.py              # DB models & connection - PostgreSQL setup
├── redis_service.py         # Redis wrapper - caching and queue management
├── storage_service.py       # MinIO wrapper - file storage operations
├── config/
│   └── settings.py          # Environment configurations
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (create this)
└── README.md               # Project documentation
```

### 🔧 Setup Instructions

#### Step 1: Install Dependencies
```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

#### Step 2: Set Up Environment Variables
Create a `.env` file in the project root with these configurations:

```env
# Database Configuration
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Authentication Settings
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# MinIO Storage Settings
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minio
MINIO_SECRET_KEY=minio123
BUCKET_NAME=document-bucket

# AI Service Configuration
GROQ_API_KEY=your_groq_api_key_here
```

#### Step 3: Start Required Services

**Option A: Using Docker (Recommended)**
```bash
# Start PostgreSQL, Redis, and MinIO using Docker Compose
docker-compose up -d postgres redis minio
```

**Option B: Manual Installation**
- Install and start PostgreSQL on port 5432
- Install and start Redis on port 6379
- Install and start MinIO on port 9000

#### Step 4: Initialize Database
```bash
# The application will automatically create tables on first run
# Or run this command to create them manually
python -c "from database import create_tables; create_tables()"
```

#### Step 5: Start the Application
```bash
# Terminal 1: Start FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start Celery worker
celery -A celery_tasks.celery_app worker --loglevel=info

# Optional Terminal 3: Start Celery monitoring
celery -A celery_tasks.celery_app flower
```

---

## 📌 API Endpoints Reference

### 🔐 Authentication Endpoints

#### Register New User
```http
POST /register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password123"
}
```

**Response:**
```json
{
  "message": "User created successfully",
  "user_id": 1
}
```

#### User Login
```http
POST /login
Content-Type: application/x-www-form-urlencoded

username=john_doe&password=secure_password123
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 📤 Document Management Endpoints

#### Upload Document
```http
POST /upload
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: multipart/form-data

file: [PDF file]
questions: "What are the main findings?\nWhat are the recommendations?" (optional)
```

**Features:**
- 🔒 Requires Bearer Token authentication
- 📎 Supports 2 uploads per minute per user (rate-limited)
- 📄 PDF files only, max size configurable
- ❓ Custom questions are optional (uses defaults if not provided)

**Response:**
```json
{
  "message": "Document uploaded successfully",
  "document_id": 42,
  "status": "pending"
}
```

#### List User Documents
```http
GET /documents
Authorization: Bearer YOUR_JWT_TOKEN
```

**Response:**
```json
{
  "documents": [
    {
      "id": 42,
      "filename": "research_paper.pdf",
      "status": "completed",
      "created_at": "2024-07-12T10:30:00Z",
      "processing_time": 45
    }
  ]
}
```

#### Get Document Details
```http
GET /documents/42
Authorization: Bearer YOUR_JWT_TOKEN
```

**Response:**
```json
{
  "id": 42,
  "filename": "research_paper.pdf",
  "status": "completed",
  "summary": "This research paper explores advanced machine learning techniques for natural language processing...",
  "qa_results": {
    "What are the main findings?": "The study found that transformer models significantly outperform traditional approaches...",
    "What are the recommendations?": "The authors recommend implementing attention mechanisms for better performance..."
  },
  "processing_time": 45,
  "created_at": "2024-07-12T10:30:00Z",
  "updated_at": "2024-07-12T10:30:45Z"
}
```

### ❤️ Health Check Endpoint

#### System Health Status
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-07-12T10:30:00Z",
  "dependencies": {
    "database": true,
    "redis": true,
    "minio": true
  },
  "version": "1.0.0"
}
```

---

## 🚀 Quick Start Guide

### 1. Get Your API Key
- Sign up at [Groq Cloud Console](https://console.groq.com)
- Generate an API key
- Add it to your `.env` file

### 2. Test the Setup
```bash
# Check if all services are running
curl http://localhost:8000/health

# Register a test user
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"test123"}'

# Login to get token
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test&password=test123"
```

### 3. Upload Your First Document
```bash
# Use the token from login response
curl -X POST http://localhost:8000/upload \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -F "file=@sample_document.pdf" \
  -F "questions=What is this document about?"
```

### 4. Check Processing Status
```bash
# Check your documents
curl http://localhost:8000/documents \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# Get specific document results
curl http://localhost:8000/documents/1 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 🔧 Configuration Options

### Environment Variables Explained

| Variable | Purpose | Example |
|----------|---------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@localhost:5432/dbname` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `SECRET_KEY` | JWT token signing key | `your_super_secret_key_here` |
| `GROQ_API_KEY` | AI service authentication | `gsk_...` |
| `MINIO_ENDPOINT` | Object storage endpoint | `localhost:9000` |
| `BUCKET_NAME` | Storage bucket name | `document-bucket` |

### Optional Configuration
```env
# Rate limiting
UPLOAD_RATE_LIMIT=2  # uploads per minute
MAX_FILE_SIZE=10485760  # 10MB in bytes

# Processing settings
DEFAULT_QUESTIONS_ENABLED=true
MAX_PROCESSING_TIME=300  # 5 minutes timeout

# Logging
LOG_LEVEL=INFO
```

---

## 📋 Requirements.txt

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
celery==5.3.4
redis==5.0.1
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
alembic==1.13.1
pydantic==2.5.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
minio==7.2.0
langchain==0.1.0
langchain-community==0.0.10
groq==0.4.1
PyPDF2==3.0.1
python-dotenv==1.0.0
structlog==23.2.0
slowapi==0.1.9
filetype==1.2.0
```

This setup guide provides everything needed to get the document processing API running locally and ready for development or production deployment.
