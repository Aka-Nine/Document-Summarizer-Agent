# ✅ Setup Checklist

## What You Have ✅

- [x] MongoDB Atlas connection string
- [x] Redis Cloud credentials
- [x] Groq API key
- [x] Gemini API key
- [x] LangChain API key
- [x] Secret key

## What You Need to Do

### 1. Create .env File
- [ ] Copy `.env.example` to `.env`
- [ ] OR manually create `.env` with your credentials

### 2. Configure Cloud Storage (REQUIRED)
Choose ONE:

**Option A: MinIO (Easiest)**
- [ ] Add to `.env`:
  ```env
  CLOUD_PROVIDER=local
  MINIO_ENDPOINT=localhost:9000
  MINIO_ACCESS_KEY=minioadmin
  MINIO_SECRET_KEY=minioadmin
  BUCKET_NAME=documents
  ```
- [ ] Start MinIO: `docker-compose up -d minio`

**Option B: AWS S3**
- [ ] Get AWS credentials
- [ ] Create S3 bucket
- [ ] Add to `.env`:
  ```env
  CLOUD_PROVIDER=aws
  AWS_REGION=us-east-1
  AWS_ACCESS_KEY_ID=your-key
  AWS_SECRET_ACCESS_KEY=your-secret
  AWS_S3_BUCKET_NAME=your-bucket
  ```

### 3. Install Dependencies
- [ ] `pip install -r requirements.txt`
- [ ] `python -m pip install "pymongo[srv]"`

### 4. Test Setup
- [ ] Run: `python test_setup.py`
- [ ] Verify all connections work

### 5. Start Application
- [ ] Run: `python run.py`
- [ ] Open: http://localhost:8000/docs

---

## 🎯 Quick Commands

```bash
# 1. Create .env (copy from .env.example)
Copy-Item .env.example .env

# 2. Install dependencies
pip install -r requirements.txt
python -m pip install "pymongo[srv]"

# 3. Start MinIO (if using local storage)
docker-compose up -d minio

# 4. Test
python test_setup.py

# 5. Start app
python run.py
```

---

## 📋 Your Credentials (Already in .env.example)

- MongoDB: `mongodb+srv://Nine:2xGBEpr60Yde3M8m@ninecluster.ltpa6.mongodb.net/`
- Redis: `rediss://:nPFMbSeVXccrygquELB6IbWWeNbSmltl@redis-14497...`
- Groq: `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`
- Gemini: `AIzaSyBDesjWhr6Y1keeL553y60sNQuEo-jNxx8`
- LangChain: `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`

---

**Just add cloud storage and you're ready!** 🚀

