# MongoDB & Redis Setup Guide

## 🎯 What You Need

### 1. **MongoDB** (Database)

#### Option A: MongoDB Atlas (Cloud - Recommended)
1. **Sign up** at https://www.mongodb.com/cloud/atlas
2. **Create a cluster** (Free tier available)
3. **Create database user** (username + password)
4. **Whitelist IP** (0.0.0.0/0 for development, specific IPs for production)
5. **Get connection string**:
   - Click "Connect" → "Connect your application"
   - Copy connection string
   - Replace `<password>` with your password

#### Option B: Local MongoDB
1. **Install MongoDB** locally or use Docker:
   ```bash
   docker run -d -p 27017:27017 --name mongodb mongo:latest
   ```
2. **Connection string**: `mongodb://localhost:27017/`

#### Option C: MongoDB on Docker Compose
Add to `docker-compose.yml`:
```yaml
mongodb:
  image: mongo:7
  ports:
    - "27017:27017"
  volumes:
    - mongodb_data:/data/db
  environment:
    MONGO_INITDB_ROOT_USERNAME: admin
    MONGO_INITDB_ROOT_PASSWORD: password
```

---

### 2. **Redis** (For Celery & Caching)

#### Option A: Redis Cloud (Recommended - Managed)
1. **Sign up** at https://redis.com/try-free/
2. **Create a database** in Redis Cloud Console
3. **Get connection details**:
   - Endpoint: `redis-xxx.cloud.redislabs.com`
   - Port: `12345` (or similar)
   - Password: From console
4. **Add to .env**:
   ```env
   REDIS_PROVIDER=redis_cloud
   REDIS_URL=rediss://:password@endpoint:port
   ```
   See `REDIS_CLOUD_SETUP.md` for detailed instructions

#### Option B: Local Redis
```bash
docker run -d -p 6379:6379 --name redis redis:7-alpine
```
```env
REDIS_PROVIDER=redis
REDIS_URL=redis://localhost:6379/0
```

#### Option C: Redis on Docker Compose
Already configured in `docker-compose.yml`
```env
REDIS_PROVIDER=redis
REDIS_URL=redis://redis:6379/0
```

---

## 📝 .env Configuration

```env
# ============================================
# SECURITY
# ============================================
SECRET_KEY=your-generated-secret-key

# ============================================
# MONGODB
# ============================================
# MongoDB Atlas (Cloud)
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=doc_intelligence

# OR Local MongoDB
# MONGODB_URL=mongodb://localhost:27017/
# MONGODB_DB_NAME=doc_intelligence

# OR Docker MongoDB
# MONGODB_URL=mongodb://admin:password@mongodb:27017/
# MONGODB_DB_NAME=doc_intelligence

# ============================================
# REDIS
# ============================================
# Redis Cloud (Recommended)
REDIS_PROVIDER=redis_cloud
REDIS_URL=rediss://:your-password@redis-xxx.cloud.redislabs.com:12345

# OR Local Redis
# REDIS_PROVIDER=redis
# REDIS_URL=redis://localhost:6379/0

# OR Docker Redis
# REDIS_PROVIDER=redis
# REDIS_URL=redis://redis:6379/0

# ============================================
# CLOUD STORAGE
# ============================================
CLOUD_PROVIDER=aws
AWS_S3_BUCKET_NAME=your-bucket
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_REGION=us-east-1

# ============================================
# LLM
# ============================================
LLM_PROVIDER=groq
GROQ_API_KEY=your-groq-key

# ============================================
# RAG (Optional)
# ============================================
RAG_ENABLED=true
VECTOR_DB_PROVIDER=pinecone
PINECONE_API_KEY=your-key
EMBEDDING_PROVIDER=openai
OPENAI_API_KEY=your-key

# ============================================
# APP SETTINGS
# ============================================
ENVIRONMENT=production
ALLOWED_ORIGINS=["http://localhost:3000"]
ALLOWED_HOSTS=["*"]
```

---

## 🚀 Quick Start

1. **Set up MongoDB**:
   - MongoDB Atlas (recommended) OR
   - Local MongoDB OR
   - Docker: `docker-compose up -d mongodb`

2. **Set up Redis**:
   - Local: `docker run -d -p 6379:6379 redis:7-alpine` OR
   - Docker Compose: `docker-compose up -d redis`

3. **Update .env** with MongoDB and Redis URLs

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run application**:
   ```bash
   python run.py
   ```

---

## 📦 Dependencies Added

Add to `requirements.txt`:
```txt
pymongo>=4.6.0
```

---

## ✅ Testing Connection

```python
# Test MongoDB
from models.mongodb_database import get_database, create_indexes
db = get_database()
print("MongoDB connected!")
create_indexes()

# Test Redis
from services.redis_service import RedisService
redis = RedisService()
redis.set_key("test", "hello")
print(redis.get_key("test"))  # Should print "hello"
```

---

## 🔄 Migration from PostgreSQL

The codebase has been updated to use MongoDB. Key changes:

1. **Models**: `models/mongodb_database.py` instead of SQLAlchemy
2. **Collections**: Users, Documents, Queries stored as MongoDB collections
3. **IDs**: MongoDB uses ObjectId (strings) instead of integers
4. **Queries**: MongoDB query syntax instead of SQL

---

## 💰 Free Tier Options

- **MongoDB Atlas**: 512MB free, shared cluster
- **Redis**: Local (free) or Redis Cloud free tier
- **AWS S3**: 5GB free for 12 months

---

**Ready?** Set up MongoDB and Redis, update `.env`, and you're good to go! 🚀

