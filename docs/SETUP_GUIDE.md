# Enterprise Document Intelligence Platform - Setup Guide

## 📋 What You Need to Provide

This guide lists all the credentials, API keys, and configuration you need to set up the platform.

---

## 🔑 Required Credentials & API Keys

### 1. **Security & Authentication**

```env
# REQUIRED: Secret key for JWT tokens (generate a strong random string)
SECRET_KEY=your-super-secret-key-minimum-32-characters-long

# Algorithm for JWT (default: HS256)
ALGORITHM=HS256

# Token expiration (default: 30 minutes)
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**How to generate SECRET_KEY:**
```python
import secrets
print(secrets.token_urlsafe(32))
```

---

### 2. **Cloud Storage Provider** (Choose ONE)

#### Option A: AWS S3 (Recommended for Production)
```env
CLOUD_PROVIDER=aws
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-aws-access-key-id
AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
AWS_S3_BUCKET_NAME=your-bucket-name
```

**Where to get:**
- AWS Console → IAM → Users → Create User → Attach `AmazonS3FullAccess` policy
- Or use existing IAM user credentials

#### Option B: MinIO (For Local Development)
```env
CLOUD_PROVIDER=local
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
BUCKET_NAME=documents
```

**Setup:**
- MinIO runs via Docker Compose (already configured)
- Default credentials: `minioadmin` / `minioadmin`

#### Option C: Azure Blob Storage (Coming Soon)
```env
CLOUD_PROVIDER=azure
AZURE_STORAGE_ACCOUNT_NAME=your-account-name
AZURE_STORAGE_ACCOUNT_KEY=your-account-key
AZURE_STORAGE_CONTAINER_NAME=documents
```

#### Option D: GCP Cloud Storage (Coming Soon)
```env
CLOUD_PROVIDER=gcp
GCP_PROJECT_ID=your-project-id
GCP_STORAGE_BUCKET_NAME=your-bucket-name
GCP_CREDENTIALS_PATH=/path/to/service-account.json
```

---

### 3. **Database** (PostgreSQL)

```env
# PostgreSQL connection string
DATABASE_URL=postgresql://username:password@host:port/database_name

# Example for Docker Compose:
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/docprocessing

# Example for AWS RDS:
DATABASE_URL=postgresql://admin:password@your-rds-endpoint.region.rds.amazonaws.com:5432/docprocessing
```

**Options:**
- **Local**: Use Docker Compose (already configured)
- **AWS RDS**: Create PostgreSQL instance in AWS
- **Azure Database**: Create PostgreSQL server in Azure
- **GCP Cloud SQL**: Create PostgreSQL instance in GCP

---

### 4. **Redis / ElastiCache**

```env
# Redis connection URL
REDIS_URL=redis://host:port/db

# Example for Docker Compose:
REDIS_URL=redis://redis:6379/0

# Example for AWS ElastiCache:
REDIS_URL=redis://your-elasticache-endpoint.cache.amazonaws.com:6379/0

# If using password:
REDIS_URL=redis://:password@host:port/db

# If using SSL:
REDIS_SSL=true
REDIS_HOST=your-redis-host
REDIS_PORT=6379
REDIS_PASSWORD=your-password
```

**Options:**
- **Local**: Use Docker Compose (already configured)
- **AWS ElastiCache**: Create Redis cluster in AWS
- **Azure Cache**: Create Redis cache in Azure
- **Redis Cloud**: Use managed Redis service

---

### 5. **Vector Database** (For RAG - Choose ONE)

#### Option A: Pinecone (Recommended)
```env
VECTOR_DB_PROVIDER=pinecone
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENVIRONMENT=us-east-1-aws  # or gcp-starter, etc.
PINECONE_INDEX_NAME=document-intelligence
```

**Where to get:**
1. Sign up at https://www.pinecone.io/
2. Create API key in dashboard
3. Note your environment (e.g., `us-east-1-aws`)

#### Option B: Qdrant (Self-hosted or Cloud)
```env
VECTOR_DB_PROVIDER=qdrant
QDRANT_URL=http://localhost:6333  # or https://your-qdrant-cloud-url
QDRANT_API_KEY=your-api-key  # Optional for local
QDRANT_COLLECTION_NAME=documents
```

**Options:**
- **Local**: Run Qdrant via Docker
- **Qdrant Cloud**: Sign up at https://cloud.qdrant.io/

#### Option C: Weaviate (Coming Soon)
```env
VECTOR_DB_PROVIDER=weaviate
WEAVIATE_URL=https://your-cluster.weaviate.network
WEAVIATE_API_KEY=your-api-key
```

---

### 6. **Embeddings Provider** (For RAG - Choose ONE)

#### Option A: OpenAI (Recommended)
```env
EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-3-small  # or text-embedding-3-large
EMBEDDING_DIMENSION=1536  # 1536 for small, 3072 for large
OPENAI_API_KEY=sk-your-openai-api-key
```

**Where to get:**
- Sign up at https://platform.openai.com/
- Create API key in dashboard
- Add billing information

#### Option B: Cohere
```env
EMBEDDING_PROVIDER=cohere
COHERE_API_KEY=your-cohere-api-key
```

**Where to get:**
- Sign up at https://cohere.com/
- Get API key from dashboard

#### Option C: HuggingFace (Free, Local)
```env
EMBEDDING_PROVIDER=huggingface
HUGGINGFACE_API_KEY=your-hf-token  # Optional for public models
HUGGINGFACE_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
```

**Where to get:**
- Sign up at https://huggingface.co/
- Get token from settings

#### Option D: AWS Bedrock
```env
EMBEDDING_PROVIDER=aws_bedrock
AWS_BEDROCK_MODEL_ID=amazon.titan-embed-text-v1
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
```

---

### 7. **LLM Provider** (For Document Processing - Choose ONE)

#### Option A: Groq (Fast & Free Tier Available)
```env
LLM_PROVIDER=groq
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama3-8b-8192  # or llama3-70b-8192, mixtral-8x7b-32768
```

**Where to get:**
- Sign up at https://console.groq.com/
- Create API key

#### Option B: OpenAI
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_LLM_MODEL=gpt-4-turbo-preview  # or gpt-3.5-turbo
OPENAI_TEMPERATURE=0.0
```

#### Option C: Anthropic Claude
```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your-anthropic-api-key
ANTHROPIC_MODEL=claude-3-opus-20240229  # or claude-3-sonnet-20240229
```

**Where to get:**
- Sign up at https://console.anthropic.com/
- Create API key

---

### 8. **RAG Configuration** (Optional)

```env
# Enable/disable RAG
RAG_ENABLED=true

# Chunking settings
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Retrieval settings
TOP_K_RETRIEVAL=5
SIMILARITY_THRESHOLD=0.7

# Reranking (optional)
RERANK_ENABLED=false
RERANK_MODEL=your-rerank-model
```

---

### 9. **Application Settings**

```env
# Environment
ENVIRONMENT=production  # or development, staging
DEBUG=false

# CORS
ALLOWED_ORIGINS=["http://localhost:3000","https://yourdomain.com"]
ALLOWED_HOSTS=["localhost","yourdomain.com","*"]

# File Upload
MAX_FILE_SIZE=52428800  # 50MB in bytes
ALLOWED_EXTENSIONS=[".pdf",".docx",".txt",".md"]
ALLOWED_MIME_TYPES=["application/pdf","application/vnd.openxmlformats-officedocument.wordprocessingml.document","text/plain","text/markdown"]

# Logging
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT=json  # json or text

# API Versioning
API_V1_PREFIX=/api/v1
```

---

### 10. **Optional: LangChain Tracing**

```env
# LangChain observability (optional)
LANGCHAIN_API_KEY=your-langchain-api-key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=Enterprise-Document-Intelligence
```

**Where to get:**
- Sign up at https://smith.langchain.com/
- Get API key

---

## 📝 Complete .env Template

Create a `.env` file in the project root:

```env
# ============================================
# SECURITY (REQUIRED)
# ============================================
SECRET_KEY=generate-this-with-secrets-token-urlsafe-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ============================================
# CLOUD STORAGE (Choose ONE)
# ============================================
CLOUD_PROVIDER=aws
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_S3_BUCKET_NAME=your-bucket

# OR for local development:
# CLOUD_PROVIDER=local
# MINIO_ENDPOINT=localhost:9000
# MINIO_ACCESS_KEY=minioadmin
# MINIO_SECRET_KEY=minioadmin
# BUCKET_NAME=documents

# ============================================
# DATABASE (REQUIRED)
# ============================================
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/docprocessing

# ============================================
# REDIS (REQUIRED)
# ============================================
REDIS_URL=redis://redis:6379/0

# ============================================
# VECTOR DATABASE (For RAG)
# ============================================
VECTOR_DB_PROVIDER=pinecone
PINECONE_API_KEY=your-pinecone-key
PINECONE_ENVIRONMENT=us-east-1-aws
PINECONE_INDEX_NAME=document-intelligence

# ============================================
# EMBEDDINGS (For RAG)
# ============================================
EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSION=1536
OPENAI_API_KEY=sk-your-openai-key

# ============================================
# LLM (For Processing)
# ============================================
LLM_PROVIDER=groq
GROQ_API_KEY=your-groq-key
GROQ_MODEL=llama3-8b-8192

# ============================================
# RAG CONFIGURATION
# ============================================
RAG_ENABLED=true
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RETRIEVAL=5
SIMILARITY_THRESHOLD=0.7

# ============================================
# APPLICATION SETTINGS
# ============================================
ENVIRONMENT=production
DEBUG=false
ALLOWED_ORIGINS=["http://localhost:3000"]
ALLOWED_HOSTS=["localhost","*"]
MAX_FILE_SIZE=52428800
ALLOWED_EXTENSIONS=[".pdf",".docx",".txt",".md"]
ALLOWED_MIME_TYPES=["application/pdf","application/vnd.openxmlformats-officedocument.wordprocessingml.document","text/plain","text/markdown"]
LOG_LEVEL=INFO
LOG_FORMAT=json
API_V1_PREFIX=/api/v1
```

---

## 🚀 Quick Start Checklist

1. ✅ **Generate SECRET_KEY**
   ```python
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. ✅ **Choose Cloud Storage Provider**
   - AWS S3 (production)
   - MinIO (local development)

3. ✅ **Set up Database**
   - Local: Docker Compose
   - Cloud: AWS RDS / Azure Database / GCP Cloud SQL

4. ✅ **Set up Redis**
   - Local: Docker Compose
   - Cloud: AWS ElastiCache / Azure Cache

5. ✅ **Choose Vector Database** (if using RAG)
   - Pinecone (easiest)
   - Qdrant (self-hosted)

6. ✅ **Choose Embeddings Provider** (if using RAG)
   - OpenAI (best quality)
   - Cohere (good alternative)
   - HuggingFace (free)

7. ✅ **Choose LLM Provider**
   - Groq (fast, free tier)
   - OpenAI (best quality)
   - Anthropic (excellent quality)

8. ✅ **Create .env file** with all credentials

9. ✅ **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

10. ✅ **Start services**
    ```bash
    docker-compose up -d postgres redis minio
    ```

11. ✅ **Run application**
    ```bash
    python run.py
    ```

---

## 💰 Cost Estimates

### Free Tier Options:
- **Groq**: Free tier available
- **HuggingFace**: Free for public models
- **Qdrant**: Free self-hosted
- **MinIO**: Free self-hosted

### Paid Options (Approximate Monthly):
- **OpenAI Embeddings**: ~$0.10 per 1M tokens
- **OpenAI GPT-4**: ~$30 per 1M input tokens
- **Pinecone**: Free tier + $70/month for starter
- **AWS S3**: ~$0.023 per GB storage
- **AWS RDS**: ~$15/month for t3.micro

---

## 🆘 Need Help?

1. Check `ENTERPRISE_UPGRADE.md` for migration details
2. Review logs for specific error messages
3. Verify all credentials are correct
4. Test each service individually (health check endpoint)

---

**Ready to start?** Follow the checklist above and you'll be up and running in minutes! 🚀

