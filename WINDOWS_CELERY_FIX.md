# Windows Celery Worker Fix - Permission Errors

**Error:** `PermissionError: [WinError 5] Access is denied` and `OSError: [WinError 6] The handle is invalid`

**Root Cause:** Celery's default multiprocessing pool doesn't work well on Windows

**Solution:** Use `--pool=solo` flag when starting Celery worker on Windows

---

## ✅ Fixed!

### 1. **Auto-Detection Added** (`app/tasks/celery_tasks.py`)
- Automatically detects Windows platform
- Sets `worker_pool=solo` for Windows (no multiprocessing)
- Uses `prefork` pool on Linux/Mac (multiprocessing)

### 2. **Startup Script Updated** (`scripts/start_celery_worker.ps1`)
- Includes `--pool=solo` flag automatically

---

## 🚀 Correct Command (Windows)

```powershell
cd d:\doc-summ-agent
$env:ENV_FILE_PATH="d:\doc-summ-agent\config\.env"
$env:PYTHONPATH="d:\doc-summ-agent"
python -c "from dotenv import load_dotenv; load_dotenv('config/.env', override=True)"
celery -A app.tasks.celery_tasks worker --loglevel=info --pool=solo
```

**Key:** The `--pool=solo` flag is required on Windows!

---

## 🔍 What is `--pool=solo`?

- **Solo Pool:** Runs tasks in the main process (no multiprocessing)
- **Windows Compatible:** No permission errors, no handle issues
- **Single Task:** One task at a time (sequential processing)
- **Perfect for:** Development and small workloads on Windows

---

## ✅ Expected Output (After Fix)

```
[tasks]
  . app.tasks.celery_tasks.process_document_task
  . app.tasks.celery_tasks.query_document_task

[INFO] Connected to redis://...
[INFO] celery@hostname ready.
```

**No more permission errors!**

---

## 🧪 Test It

1. **Stop any running worker** (Ctrl+C)

2. **Start with solo pool:**
   ```powershell
   celery -A app.tasks.celery_tasks worker --loglevel=info --pool=solo
   ```

3. **Upload a document** via API

4. **Watch worker process it** - Should work without errors!

---

## 📊 Pool Options

### Windows (Current Setup)
```powershell
--pool=solo
```
- ✅ No multiprocessing issues
- ✅ Works reliably
- ⚠️ One task at a time

### Windows (If you need concurrency)
```powershell
--pool=threads
```
- ✅ Multiple tasks concurrently
- ✅ Windows compatible
- ⚠️ GIL limitations

### Linux/Mac (Production)
```bash
--pool=prefork --concurrency=4
```
- ✅ True multiprocessing
- ✅ Multiple CPU cores
- ❌ Doesn't work on Windows

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

**Windows (Recommended):**
```powershell
celery -A app.tasks.celery_tasks worker --pool=solo --loglevel=info
```

**Or use the script:**
```powershell
.\scripts\start_celery_worker.ps1
```

The script now includes `--pool=solo` automatically!

