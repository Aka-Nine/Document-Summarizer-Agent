# Quick Start: Celery Worker

## ✅ Correct Command to Start Worker (Windows)

```powershell
cd d:\doc-summ-agent
$env:ENV_FILE_PATH="d:\doc-summ-agent\config\.env"
$env:PYTHONPATH="d:\doc-summ-agent"
python -c "from dotenv import load_dotenv; load_dotenv('config/.env', override=True)"
celery -A app.tasks.celery_tasks worker --loglevel=info --pool=solo
```

**Important:** Use `--pool=solo` on Windows to avoid multiprocessing permission errors!

---

## 🔍 What This Does

1. **Sets environment variables** - ENV_FILE_PATH and PYTHONPATH
2. **Loads .env file** - Before Celery imports settings
3. **Starts Celery worker** - Using standard celery command (not worker_main)

---

## ✅ Expected Output

```
[tasks]
  . app.tasks.celery_tasks.process_document_task
  . app.tasks.celery_tasks.query_document_task

[INFO] Connected to redis://...
[INFO] celery@hostname ready.
```

---

## 🚨 If You Get Errors

### "SECRET_KEY Field required"
→ Make sure you run the `load_dotenv` command first

### "No module named 'app'"
→ Make sure PYTHONPATH is set to project root

### "ValueError: not enough values to unpack"
→ Use `celery` command directly, not `worker_main()`

---

## 📝 One-Line Version

```powershell
cd d:\doc-summ-agent; $env:ENV_FILE_PATH="d:\doc-summ-agent\config\.env"; $env:PYTHONPATH="d:\doc-summ-agent"; python -c "from dotenv import load_dotenv; load_dotenv('config/.env', override=True)"; celery -A app.tasks.celery_tasks worker --loglevel=info
```

---

## ✅ That's It!

Once the worker is running, documents will be processed automatically when uploaded.

