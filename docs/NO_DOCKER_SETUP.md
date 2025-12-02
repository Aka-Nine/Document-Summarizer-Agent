# 🚀 Setup Without Docker - Filesystem Storage

## ✅ What's Changed

1. **Gemini is now PRIMARY LLM** (instead of Groq)
2. **Filesystem Storage Added** - No Docker needed!
3. **Works without Docker** - Perfect for development

---

## 📋 Quick Setup

### 1. Create .env File

Copy `.env.example` to `.env` and it's already configured for:
- ✅ Gemini (primary LLM)
- ✅ Filesystem storage (no Docker)
- ✅ MongoDB Atlas
- ✅ Redis Cloud

### 2. Install Dependencies

```bash
pip install -r requirements.txt
python -m pip install "pymongo[srv]"
```

### 3. Run!

```bash
python run.py
```

**That's it!** No Docker needed! 🎉

---

## 📁 Filesystem Storage

Files are stored in the `storage/` directory (created automatically).

**Features:**
- ✅ No Docker required
- ✅ Files stored locally
- ✅ Accessible via `/files/{path}` endpoint
- ✅ Works immediately

**Storage Location:**
- Default: `storage/` directory in project root
- Configurable via `FILESYSTEM_STORAGE_PATH` in `.env`

---

## 🔧 Configuration

Your `.env` should have:

```env
# LLM - Gemini is primary
LLM_PROVIDER=gemini
GEMINI_API_KEY=AIzaSyBDesjWhr6Y1keeL553y60sNQuEo-jNxx8
GEMINI_MODEL=gemini-pro

# Storage - Filesystem (no Docker)
CLOUD_PROVIDER=filesystem
FILESYSTEM_STORAGE_PATH=storage
FILESYSTEM_BASE_URL=http://localhost:8000/files

# MongoDB & Redis (already configured)
MONGODB_URL=mongodb+srv://...
REDIS_URL=rediss://...
```

---

## 🎯 What You Get

- ✅ **Gemini LLM** - Primary AI model
- ✅ **Filesystem Storage** - No Docker needed
- ✅ **MongoDB Atlas** - Cloud database
- ✅ **Redis Cloud** - Cloud cache/queue
- ✅ **Everything works** - No local services needed!

---

## 💡 Switching Back to Groq

If you want to use Groq instead:

```env
LLM_PROVIDER=groq
GROQ_API_KEY=your-groq-key
```

---

## 📝 File Access

Files uploaded are accessible at:
```
http://localhost:8000/files/{user_id}/{file_id}.{ext}
```

The system automatically generates these URLs when files are uploaded.

---

**Ready to go!** Just install dependencies and run! 🚀

