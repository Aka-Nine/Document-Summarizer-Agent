# 🚀 Quick Start Guide

## What You Need to Provide

### **MUST HAVE (Required):**

1. **SECRET_KEY** - Generate with:
   ```python
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **MongoDB** - MongoDB connection string
   - Local: `mongodb://localhost:27017/`
   - MongoDB Atlas: `mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority`
   - Docker: `mongodb://admin:password@mongodb:27017/`

3. **Redis** - Redis connection URL
   - Local: `redis://localhost:6379/0`
   - Docker: `redis://redis:6379/0`
   - Cloud: Your Redis Cloud/ElastiCache connection string

4. **Cloud Storage** - Choose ONE:
   - **AWS S3**: Access key, secret key, bucket name
   - **MinIO** (local): Already configured in Docker Compose

5. **LLM Provider** - Choose ONE:
   - **Groq**: Free API key from https://console.groq.com/
   - **OpenAI**: API key from https://platform.openai.com/
   - **Anthropic**: API key from https://console.anthropic.com/

### **FOR RAG (Optional but Recommended):**

6. **Vector Database** - Choose ONE:
   - **Pinecone**: Free tier at https://www.pinecone.io/
   - **Qdrant**: Self-hosted or cloud

7. **Embeddings Provider** - Choose ONE:
   - **OpenAI**: Same API key as LLM
   - **Cohere**: Free tier at https://cohere.com/
   - **HuggingFace**: Free for public models

---

## 📝 Minimal .env File (Get Started Fast)

```env
# REQUIRED
SECRET_KEY=your-generated-secret-key-here
MONGODB_URL=mongodb://localhost:27017/
MONGODB_DB_NAME=doc_intelligence
REDIS_URL=redis://localhost:6379/0

# Cloud Storage (MinIO for local)
CLOUD_PROVIDER=local
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
BUCKET_NAME=documents

# LLM (Groq - easiest to get started)
LLM_PROVIDER=groq
GROQ_API_KEY=your-groq-api-key

# Basic Settings
ALLOWED_ORIGINS=["http://localhost:3000"]
ALLOWED_HOSTS=["localhost","*"]
MAX_FILE_SIZE=52428800
ALLOWED_EXTENSIONS=[".pdf",".docx",".txt"]
ALLOWED_MIME_TYPES=["application/pdf","application/vnd.openxmlformats-officedocument.wordprocessingml.document","text/plain"]
```

**To enable RAG, add:**
```env
RAG_ENABLED=true
VECTOR_DB_PROVIDER=pinecone
PINECONE_API_KEY=your-key
PINECONE_ENVIRONMENT=us-east-1-aws
EMBEDDING_PROVIDER=openai
OPENAI_API_KEY=your-key
```

---

## ⚡ 5-Minute Setup

1. **Generate SECRET_KEY:**
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Get Groq API Key:**
   - Go to https://console.groq.com/
   - Sign up (free)
   - Create API key

3. **Create .env file** with the minimal config above

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Start services:**
   ```bash
   docker-compose up -d mongodb redis minio
   ```

6. **Run the app:**
   ```bash
   python run.py
   ```

7. **Test it:**
   - Open http://localhost:8000/docs
   - Register a user
   - Upload a document
   - Query it!

---

## 📚 Full Documentation

- **SETUP_GUIDE.md** - Complete setup with all options
- **ENTERPRISE_UPGRADE.md** - Migration and upgrade guide
- **README.md** - General documentation

---

## 🎯 What Each Service Does

- **PostgreSQL**: Stores user data, documents, metadata
- **Redis**: Task queue for Celery, caching
- **MinIO/S3**: File storage for uploaded documents
- **Vector DB**: Stores document embeddings for RAG search
- **Embeddings**: Converts text to vectors for similarity search
- **LLM**: Processes documents, generates summaries, answers questions

---

**Ready?** Start with the minimal .env above and expand as needed! 🚀

