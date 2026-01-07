# Quick Start: Celery Worker

## 🚀 Start Worker (One Command)

```powershell
cd d:\doc-summ-agent; .\scripts\start_celery_worker.ps1
```

Or manually:

```powershell
cd d:\doc-summ-agent
$env:ENV_FILE_PATH="d:\doc-summ-agent\config\.env"
$env:PYTHONPATH="d:\doc-summ-agent"
python -c "from dotenv import load_dotenv; load_dotenv('config/.env', override=True)"
celery -A app.tasks.celery_tasks worker --loglevel=info --pool=solo
```

---

## ✅ Verify Worker is Running

Look for these lines in the output:

```
[tasks]
  . process_document_task
  . query_document_task

celery@HOSTNAME ready.
```

---

## 🧪 Test It

1. **Keep worker running** in one terminal
2. **Upload a document** via API in another terminal
3. **Watch worker logs** - you should see task execution

---

## ❌ If Tasks Still Not Picking Up

1. **Check worker is running**: Look for "celery@HOSTNAME ready"
2. **Check Redis connection**: Look for "Connected to redis://..."
3. **Check task registration**: Look for task list in worker startup
4. **Restart worker** after any code changes

