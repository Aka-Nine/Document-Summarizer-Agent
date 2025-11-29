# 🎯 Your Complete Setup Guide

## ✅ What's Already Configured

All your credentials are ready! Here's what you have:

1. ✅ **MongoDB Atlas**: `mongodb+srv://Nine:2xGBEpr60Yde3M8m@ninecluster.ltpa6.mongodb.net/`
2. ✅ **Redis Cloud**: `redis-14497.c325.us-east-1-4.ec2.cloud.redislabs.com:14497`
3. ✅ **Groq API**: Ready to use
4. ✅ **Gemini API**: Ready (alternative option)
5. ✅ **LangChain**: Configured
6. ✅ **Secret Key**: Set

---

## ⚠️ What You Need to Add

### **Cloud Storage** (REQUIRED - Choose ONE)

#### Option 1: MinIO (Easiest for Development) ✅ Recommended to Start

1. **Start MinIO**:
   ```bash
   docker-compose up -d minio
   ```

2. **Add to your `.env` file**:
   ```env
   CLOUD_PROVIDER=local
   MINIO_ENDPOINT=localhost:9000
   MINIO_ACCESS_KEY=minioadmin
   MINIO_SECRET_KEY=minioadmin
   BUCKET_NAME=documents
   ```

3. **Access MinIO Console**: http://localhost:9001
   - Login: `minioadmin` / `minioadmin`

#### Option 2: AWS S3 (For Production)

1. **Get AWS Credentials**:
   - Go to AWS Console → IAM → Create User
   - Attach `AmazonS3FullAccess` policy
   - Create Access Key

2. **Create S3 Bucket**:
   - Go to S3 → Create Bucket
   - Choose region (e.g., `us-east-1`)

3. **Add to `.env`**:
   ```env
   CLOUD_PROVIDER=aws
   AWS_REGION=us-east-1
   AWS_ACCESS_KEY_ID=your-aws-access-key
   AWS_SECRET_ACCESS_KEY=your-aws-secret-key
   AWS_S3_BUCKET_NAME=your-bucket-name
   ```

---

## 🚀 Quick Start (3 Steps)

### Step 1: Create .env File

Copy `.env.example` to `.env`:
```bash
# Windows PowerShell
Copy-Item .env.example .env

# Or manually copy the file
```

Then **edit `.env`** and add cloud storage configuration (see above).

### Step 2: Install Dependencies

```bash
# Install all packages
pip install -r requirements.txt

# Install MongoDB SRV support (important!)
python -m pip install "pymongo[srv]"
```

### Step 3: Start & Test

**If using MinIO**:
```bash
# Start MinIO
docker-compose up -d minio

# Test your setup
python test_setup.py

# Start the application
python run.py
```

**If using AWS S3**:
```bash
# Just test and start (no local services needed)
python test_setup.py
python run.py
```

---

## 📝 Complete .env File Template

Create a `.env` file with this content:

```env
# ============================================
# SECURITY
# ============================================
SECRET_KEY=Dz9pciTZVR4p2GmtAUmVsuiOUMfxyccu3q0WvFf8-Qc
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ============================================
# MONGODB
# ============================================
MONGODB_URL=mongodb+srv://Nine:2xGBEpr60Yde3M8m@ninecluster.ltpa6.mongodb.net/?appName=NIneCluster
MONGODB_DB_NAME=doc_intelligence

# ============================================
# REDIS CLOUD
# ============================================
REDIS_PROVIDER=redis_cloud
REDIS_URL=rediss://:nPFMbSeVXccrygquELB6IbWWeNbSmltl@redis-14497.c325.us-east-1-4.ec2.cloud.redislabs.com:14497

# ============================================
# CLOUD STORAGE (CHOOSE ONE)
# ============================================
# Option 1: MinIO (Local - Easiest)
CLOUD_PROVIDER=local
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
BUCKET_NAME=documents

# Option 2: AWS S3 (Production)
# CLOUD_PROVIDER=aws
# AWS_REGION=us-east-1
# AWS_ACCESS_KEY_ID=your-aws-key
# AWS_SECRET_ACCESS_KEY=your-aws-secret
# AWS_S3_BUCKET_NAME=your-bucket

# ============================================
# LLM
# ============================================
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama3-8b-8192

# Gemini (Alternative)
# LLM_PROVIDER=gemini
# GEMINI_API_KEY=AIzaSyBDesjWhr6Y1keeL553y60sNQuEo-jNxx8
# GEMINI_MODEL=gemini-pro

# ============================================
# LANGCHAIN
# ============================================
LANGCHAIN_API_KEY=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
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=Enterprise-Document-Intelligence

# ============================================
# RAG (OPTIONAL - Disabled by default)
# ============================================
RAG_ENABLED=false

# ============================================
# APP SETTINGS
# ============================================
ENVIRONMENT=production
DEBUG=false
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:8000"]
ALLOWED_HOSTS=["localhost","*"]
MAX_FILE_SIZE=52428800
ALLOWED_EXTENSIONS=[".pdf",".docx",".txt",".md"]
ALLOWED_MIME_TYPES=["application/pdf","application/vnd.openxmlformats-officedocument.wordprocessingml.document","text/plain","text/markdown"]
LOG_LEVEL=INFO
LOG_FORMAT=json
API_V1_PREFIX=/api/v1
```

---

## 🧪 Test Your Setup

Run the test script:
```bash
python test_setup.py
```

This will check:
- ✅ MongoDB connection
- ✅ Redis connection
- ✅ LLM configuration
- ⚠️ Cloud storage (will show what's missing)
- ℹ️ RAG (optional)

---

## 🎯 What's Missing Summary

### Required:
1. **Cloud Storage** - Choose MinIO (easiest) or AWS S3

### Optional (For RAG):
- Vector Database (Pinecone, Qdrant, etc.)
- Embeddings Provider (OpenAI, Cohere, etc.)

**You can start without RAG** - just set `RAG_ENABLED=false` in `.env`

---

## 🚀 Ready to Start?

1. **Create `.env` file** (copy from `.env.example` or use template above)
2. **Add cloud storage** (MinIO or AWS S3)
3. **Install**: `pip install -r requirements.txt && python -m pip install "pymongo[srv]"`
4. **Test**: `python test_setup.py`
5. **Start**: `python run.py`
6. **Access**: http://localhost:8000/docs

---

## 💡 Pro Tips

- **Start with MinIO** - It's the easiest way to get started
- **RAG is optional** - You can add it later
- **Gemini is ready** - Switch by changing `LLM_PROVIDER=gemini`
- **All your credentials are in `.env.example`** - Just copy and add storage!

---

**You're almost there!** Just add cloud storage and you're ready to go! 🚀

