# Celery Worker Startup Fix

**Error:** `SECRET_KEY Field required` when starting Celery worker

**Root Cause:** Environment variables from `.env` file aren't loaded before Settings initialization

---

## ✅ Solution 1: Use the Fixed Script (Recommended)

The `scripts/celery_worker.py` script has been updated to load environment variables before importing anything.

### Start Worker:
```powershell
cd d:\doc-summ-agent
$env:ENV_FILE_PATH="d:\doc-summ-agent\config\.env"
$env:PYTHONPATH="d:\doc-summ-agent"
python scripts/celery_worker.py
```

Or use the PowerShell script:
```powershell
.\scripts\start_celery_worker.ps1
```

---

## ✅ Solution 2: Use Celery Command with Environment Variables

If you prefer using the standard `celery` command:

```powershell
cd d:\doc-summ-agent

# Set environment variables
$env:ENV_FILE_PATH="d:\doc-summ-agent\config\.env"
$env:PYTHONPATH="d:\doc-summ-agent"

# Load .env file manually first
python -c "from dotenv import load_dotenv; load_dotenv('config\.env', override=True)"

# Then start celery (in same session)
celery -A app.tasks.celery_tasks worker --loglevel=info
```

---

## ✅ Solution 3: Set Environment Variables Manually

If the above don't work, you can set critical variables manually:

```powershell
cd d:\doc-summ-agent
$env:ENV_FILE_PATH="d:\doc-summ-agent\config\.env"
$env:PYTHONPATH="d:\doc-summ-agent"
$env:SECRET_KEY="your-secret-key-from-env"
$env:MONGODB_URL="your-mongodb-url"
$env:REDIS_URL="your-redis-url"
# ... set other required vars

celery -A app.tasks.celery_tasks worker --loglevel=info
```

---

## 🔍 What Was Fixed

The `scripts/celery_worker.py` script now:

1. **Loads .env file FIRST** - Before importing any app modules
2. **Sets ENV_FILE_PATH** - So pydantic settings can find the .env file
3. **Sets PYTHONPATH** - So Python can find the app modules
4. **Then imports Celery app** - After environment is ready

---

## ✅ Verification

When the worker starts successfully, you should see:

```
Loaded environment from: D:\doc-summ-agent\config\.env
[tasks]
  . app.tasks.celery_tasks.process_document_task
  . app.tasks.celery_tasks.query_document_task

[INFO] Connected to redis://...
[INFO] celery@hostname ready.
```

---

## 🚨 If You Still Get Errors

### Error: "SECRET_KEY Field required"
- Make sure `.env` file exists at `config/.env`
- Check that `SECRET_KEY` is set in the `.env` file
- Verify `ENV_FILE_PATH` environment variable points to the `.env` file

### Error: "No module named 'app'"
- Set `PYTHONPATH` to project root: `$env:PYTHONPATH="d:\doc-summ-agent"`
- Make sure you're in the project directory

### Error: "Redis connection failed"
- Check Redis is running and accessible
- Verify Redis configuration in `.env` file
- Test Redis connection separately

---

## 📝 Quick Start Command

**Simplest way to start the worker:**

```powershell
cd d:\doc-summ-agent
$env:ENV_FILE_PATH="d:\doc-summ-agent\config\.env"
$env:PYTHONPATH="d:\doc-summ-agent"
python scripts/celery_worker.py
```

This will:
- ✅ Load environment variables automatically
- ✅ Start the Celery worker
- ✅ Process queued document tasks

---

## ✅ Summary

**The Fix:** Updated `scripts/celery_worker.py` to load `.env` file before importing app modules

**The Command:** `python scripts/celery_worker.py`

**The Result:** Worker starts successfully and processes documents!

