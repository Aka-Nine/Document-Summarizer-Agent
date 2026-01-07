# Celery Windows Compatibility Fix

**Error:** `PermissionError: [WinError 5] Access is denied` and `OSError: [WinError 6] The handle is invalid`

**Root Cause:** Celery's default multiprocessing pool (`prefork`/`spawn`) has issues on Windows

**Solution:** Use `--pool=solo` for Windows (runs tasks in main process, no multiprocessing)

---

## ✅ Fixed Configuration

### 1. **Celery Configuration Updated** (`app/tasks/celery_tasks.py`)
- Automatically detects Windows and uses `solo` pool
- On Linux/Mac, uses `prefork` pool (multiprocessing)

### 2. **Startup Script Updated** (`scripts/start_celery_worker.ps1`)
- Uses `--pool=solo` flag for Windows compatibility

---

## 🚀 Correct Command to Start Worker (Windows)

```powershell
cd d:\doc-summ-agent
$env:ENV_FILE_PATH="d:\doc-summ-agent\config\.env"
$env:PYTHONPATH="d:\doc-summ-agent"
python -c "from dotenv import load_dotenv; load_dotenv('config/.env', override=True)"
celery -A app.tasks.celery_tasks worker --loglevel=info --pool=solo
```

**Important:** The `--pool=solo` flag is required on Windows!

---

## 🔍 What is `--pool=solo`?

- **Solo Pool:** Runs tasks in the main process (no multiprocessing)
- **Pros:** Works perfectly on Windows, no permission issues
- **Cons:** Single-threaded (one task at a time)
- **Use Case:** Development and small-scale production on Windows

---

## 📊 Pool Options

### For Windows (Current Setup)
```powershell
celery -A app.tasks.celery_tasks worker --pool=solo --loglevel=info
```
- ✅ No multiprocessing issues
- ✅ Works reliably on Windows
- ⚠️ Single task at a time

### Alternative: Threads Pool (Windows)
```powershell
celery -A app.tasks.celery_tasks worker --pool=threads --loglevel=info
```
- ✅ Multiple tasks concurrently
- ✅ Windows compatible
- ⚠️ GIL limitations (Python threads)

### For Linux/Mac (Production)
```bash
celery -A app.tasks.celery_tasks worker --pool=prefork --loglevel=info --concurrency=4
```
- ✅ True multiprocessing
- ✅ Multiple CPU cores
- ❌ Doesn't work on Windows

---

## ✅ Expected Output (After Fix)

When started correctly with `--pool=solo`, you should see:

```
[tasks]
  . app.tasks.celery_tasks.process_document_task
  . app.tasks.celery_tasks.query_document_task

[INFO] Connected to redis://...
[INFO] celery@hostname ready.
```

**No more permission errors!**

---

## 🧪 Testing

1. **Start Worker:**
   ```powershell
   celery -A app.tasks.celery_tasks worker --loglevel=info --pool=solo
   ```

2. **Upload a Document:**
   ```bash
   POST /api/v1/documents/upload
   ```

3. **Watch Worker Process:**
   - Should see: `Task process_document_task[...] received`
   - Should see: `Document processing started`
   - Should see: `Document processing completed`
   - **No permission errors!**

---

## 📝 Updated Files

1. **`app/tasks/celery_tasks.py`**
   - Auto-detects Windows and uses `solo` pool
   - Configurable via `worker_pool` setting

2. **`scripts/start_celery_worker.ps1`**
   - Includes `--pool=solo` flag

3. **`QUICK_START_CELERY.md`**
   - Updated with Windows-specific command

---

## ⚠️ Important Notes

### Solo Pool Limitations
- **Single task at a time** - Tasks run sequentially
- **No parallel processing** - One document processes at a time
- **Fine for development** - Perfect for testing and small workloads

### For Production on Windows
If you need concurrent processing on Windows:
- Use `--pool=threads` (multiple tasks, but GIL limited)
- Or deploy on Linux/Mac where `prefork` works perfectly

### For Production Deployment
- **Linux/Mac:** Use `--pool=prefork --concurrency=4` (or more)
- **Windows:** Use `--pool=solo` or `--pool=threads`

---

## ✅ Summary

**The Problem:** Windows multiprocessing permission errors

**The Solution:** Use `--pool=solo` on Windows

**The Command:**
```powershell
celery -A app.tasks.celery_tasks worker --loglevel=info --pool=solo
```

**The Result:** Worker runs without errors and processes documents!

---

## 🔄 Quick Reference

**Windows (Development):**
```powershell
celery -A app.tasks.celery_tasks worker --pool=solo --loglevel=info
```

**Windows (If you need concurrency):**
```powershell
celery -A app.tasks.celery_tasks worker --pool=threads --loglevel=info
```

**Linux/Mac (Production):**
```bash
celery -A app.tasks.celery_tasks worker --pool=prefork --concurrency=4 --loglevel=info
```

