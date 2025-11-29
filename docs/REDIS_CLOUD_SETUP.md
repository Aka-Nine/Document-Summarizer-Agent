# Redis Cloud Setup Guide

## 🎯 Using Redis Cloud Console

Redis Cloud provides a managed Redis service with easy setup through their console.

---

## 📋 How to Get Your Redis Cloud Connection

### Step 1: Sign Up / Log In
1. Go to https://redis.com/try-free/ or https://redis.com/cloud/
2. Sign up or log in to Redis Cloud Console

### Step 2: Create a Database
1. In Redis Cloud Console, click **"New Database"** or **"Create Database"**
2. Choose your plan (Free tier available)
3. Select region
4. Click **"Create Database"**

### Step 3: Get Connection Details
1. Click on your database
2. You'll see connection details:
   - **Endpoint**: `redis-12345.c1.us-east-1-1.ec2.cloud.redislabs.com`
   - **Port**: `12345` (or similar)
   - **Password**: Click "Show" to reveal password
   - **SSL**: Enabled (required)

### Step 4: Configure in .env

**Option A: Using REDIS_URL (Recommended)**
```env
REDIS_PROVIDER=redis_cloud
REDIS_URL=rediss://:your-password@redis-12345.c1.us-east-1-1.ec2.cloud.redislabs.com:12345
```

**Option B: Using Individual Settings**
```env
REDIS_PROVIDER=redis_cloud
REDIS_CLOUD_ENDPOINT=redis-12345.c1.us-east-1-1.ec2.cloud.redislabs.com
REDIS_CLOUD_PORT=12345
REDIS_CLOUD_PASSWORD=your-password-here
REDIS_CLOUD_SSL=true
```

---

## 🔑 Connection String Format

Redis Cloud connection string format:
```
rediss://:password@endpoint:port
```

**Note**: 
- Use `rediss://` (with double 's') for SSL
- Password comes after `:` and before `@`
- No username needed (just password)

---

## 📝 Complete .env Example

```env
# ============================================
# SECURITY
# ============================================
SECRET_KEY=your-generated-secret-key

# ============================================
# MONGODB
# ============================================
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=doc_intelligence

# ============================================
# REDIS CLOUD
# ============================================
REDIS_PROVIDER=redis_cloud
REDIS_URL=rediss://:your-redis-cloud-password@redis-12345.c1.us-east-1-1.ec2.cloud.redislabs.com:12345

# OR use individual settings:
# REDIS_CLOUD_ENDPOINT=redis-12345.c1.us-east-1-1.ec2.cloud.redislabs.com
# REDIS_CLOUD_PORT=12345
# REDIS_CLOUD_PASSWORD=your-password
# REDIS_CLOUD_SSL=true

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
```

---

## ✅ Testing Connection

Test your Redis Cloud connection:

```python
from services.redis_service import RedisService

redis = RedisService()
redis.set_key("test", "hello")
print(redis.get_key("test"))  # Should print "hello"
print("✅ Redis Cloud connected!")
```

---

## 🔧 For Celery

Celery will automatically use the same Redis connection. The `REDIS_URL` is used for both:
- Application caching (RedisService)
- Celery broker and backend

---

## 🆘 Troubleshooting

### Connection Issues:
1. **Check SSL**: Redis Cloud requires SSL (`rediss://` not `redis://`)
2. **Verify Password**: Make sure password is correct (no extra spaces)
3. **Check Endpoint**: Ensure endpoint and port are correct
4. **Whitelist IP**: Some Redis Cloud plans require IP whitelisting

### SSL Certificate Issues:
If you get SSL errors, the code automatically handles SSL certificates for Redis Cloud.

---

## 💰 Redis Cloud Pricing

- **Free Tier**: 30MB, perfect for development
- **Fixed Plans**: Starting at $10/month
- **Pay-as-you-go**: Based on usage

---

## 📚 Resources

- **Redis Cloud Console**: https://redis.com/cloud/
- **Redis Cloud Docs**: https://docs.redis.com/
- **Connection Guide**: https://docs.redis.com/latest/rc/rc-quickstart/

---

**Ready?** Get your connection string from Redis Cloud Console and add it to `.env`! 🚀

