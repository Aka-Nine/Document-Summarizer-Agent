# Celery Worker - Correct Startup Method

**Error Fixed:** `ValueError: not enough values to unpack (expected 3, got 0)`

**Solution:** Use standard `celery` command instead of `worker_main()`

---

## ✅ Correct Way to Start Celery Worker

### Method 1: Direct Celery Command (Recommended)

```powershell
cd d:\doc-summ-agent

# Set environment variables
$env:ENV_FILE_PATH="d:\doc-summ-agent\config\.env"
$env:PYTHONPATH="d:\doc-summ-agent"

# Load .env file first
python -c "from dotenv import load_dotenv; load_dotenv('config\.env', override=True)"

# Start Celery worker
celery -A app.tasks.celery_tasks worker --loglevel=info
```

### Method 2: One-Line Command

```powershell
cd d:\doc-summ-agent; $env:ENV_FILE_PATH="d:\doc-summ-agent\config\.env"; $env:PYTHONPATH="d:\doc-summ-agent"; python -c "from dotenv import load_dotenv; load_dotenv('config\.env', override=True)"; celery -A app.tasks.celery_tasks worker --loglevel=info
```

### Method 3: Updated PowerShell Script

The `scripts/start_celery_worker.ps1` has been updated to use this method.

```powershell
.\scripts\start_celery_worker.ps1
```

---

## 🔍 Why This Works

1. **Loads .env file first** - Before Celery tries to import settings
2. **Uses standard celery command** - More reliable than `worker_main()`
3. **Proper argument handling** - Celery CLI handles arguments correctly
4. **Environment variables set** - ENV_FILE_PATH and PYTHONPATH configured

---

## ✅ Expected Output

When started correctly, you should see:

```
[tasks]
  . app.tasks.celery_tasks.process_document_task
  . app.tasks.celery_tasks.query_document_task

[2026-01-04 20:00:00,000: INFO/MainProcess] Connected to redis://...
[2026-01-04 20:00:00,000: INFO/MainProcess] celery@hostname ready.
```

---

## 🚨 Common Errors and Fixes

### Error: "SECRET_KEY Field required"
**Fix:** Make sure `.env` file is loaded before starting:
```powershell
python -c "from dotenv import load_dotenv; load_dotenv('config\.env', override=True)"
```

### Error: "No module named 'app'"
**Fix:** Set PYTHONPATH:
```powershell
$env:PYTHONPATH="d:\doc-summ-agent"
```

### Error: "ValueError: not enough values to unpack"
**Fix:** Use `celery` command directly, not `worker_main()`

---

## 📝 Quick Reference

**Start Worker:**
```powershell
cd d:\doc-summ-agent
$env:ENV_FILE_PATH="d:\doc-summ-agent\config\.env"
$env:PYTHONPATH="d:\doc-summ-agent"
python -c "from dotenv import load_dotenv; load_dotenv('config\.env', override=True)"
celery -A app.tasks.celery_tasks worker --loglevel=info
```

**Stop Worker:**
Press `Ctrl+C` in the terminal where worker is running

**Check Worker Status:**
Look for "celery@hostname ready" message

---

## ✅ Summary

**The Fix:** Use standard `celery` command instead of `worker_main()`

**The Command:**
```powershell
celery -A app.tasks.celery_tasks worker --loglevel=info
```

**The Result:** Worker starts successfully without unpacking errors!

