# Start Celery Worker - Document Processing Guide

**Issue:** Documents are uploaded to MongoDB but not processed (no summaries, no vector indexing, no RAG)

**Root Cause:** Celery worker is not running to process the queued tasks

---

## 🚀 Quick Start

### Step 1: Open a New Terminal

Keep your API server running in one terminal, and open a **new terminal window** for the Celery worker.

### Step 2: Navigate to Project Directory

```powershell
cd d:\doc-summ-agent
```

### Step 3: Activate Virtual Environment (if using one)

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 4: Set Environment Variables

```powershell
$env:ENV_FILE_PATH="d:\doc-summ-agent\config\.env"
$env:PYTHONPATH="d:\doc-summ-agent"
```

### Step 5: Start Celery Worker

```powershell
celery -A app.tasks.celery_tasks worker --loglevel=info
```

---

## ✅ What You Should See

When the Celery worker starts successfully, you'll see:

```
[tasks]
  . app.tasks.celery_tasks.process_document_task
  . app.tasks.celery_tasks.query_document_task

[2026-01-04 20:00:00,000: INFO/MainProcess] Connected to redis://...
[2026-01-04 20:00:00,000: INFO/MainProcess] celery@hostname ready.
```

---

## 📋 What Happens When Worker Runs

1. **Document Upload** → Stored in MongoDB + Queued in Redis
2. **Celery Worker** → Picks up task from Redis queue
3. **Processing** → Downloads file, processes with LLM, generates summary
4. **RAG Indexing** → Chunks document, creates embeddings, stores in Chroma
5. **Update MongoDB** → Saves summary, QA results, processing status

---

## 🔍 Verify Worker is Running

### Check 1: Worker Logs
You should see messages like:
```
[INFO] Received task: process_document_task[document-id-123]
[INFO] Document processing started
[INFO] Document processing completed
```

### Check 2: Document Status
After uploading a document, check its status:
```bash
GET /api/v1/documents/{document_id}
```

Status should change:
- `pending` → `processing` → `completed`

### Check 3: Check Redis Queue
```python
from app.services.redis_service import RedisService
redis = RedisService()
# Check if tasks are queued
```

---

## 🛠️ Troubleshooting

### Issue: "No module named 'app'"
**Solution:**
```powershell
$env:PYTHONPATH="d:\doc-summ-agent"
```

### Issue: "Redis connection failed"
**Solution:**
- Check Redis is running and accessible
- Verify Redis configuration in `.env`
- Test Redis connection: `python -c "from app.services.redis_service import RedisService; RedisService()"`

### Issue: "Tasks queued but not processing"
**Solution:**
- Verify worker is connected to same Redis instance
- Check worker logs for errors
- Ensure worker has access to same environment variables

### Issue: "Import errors"
**Solution:**
- Make sure virtual environment is activated
- Install dependencies: `pip install -r config/requirements.txt`
- Check PYTHONPATH is set

---

## 📊 Monitor Worker Activity

### Option 1: Worker Logs
Watch the terminal where worker is running - you'll see all task processing in real-time.

### Option 2: Flower (Optional)
Start Flower monitoring UI:
```powershell
celery -A app.tasks.celery_tasks flower --port=5555
```
Then visit: http://localhost:5555

### Option 3: Check Document Status via API
```bash
GET /api/v1/documents/{document_id}
```
Watch the `status` field change from `pending` → `processing` → `completed`

---

## 🔄 Complete Workflow

### Terminal 1: API Server
```powershell
cd d:\doc-summ-agent
$env:ENV_FILE_PATH="d:\doc-summ-agent\config\.env"
$env:PYTHONPATH="d:\doc-summ-agent"
python run.py
```

### Terminal 2: Celery Worker
```powershell
cd d:\doc-summ-agent
$env:ENV_FILE_PATH="d:\doc-summ-agent\config\.env"
$env:PYTHONPATH="d:\doc-summ-agent"
celery -A app.tasks.celery_tasks worker --loglevel=info
```

### Terminal 3: (Optional) Flower Monitor
```powershell
cd d:\doc-summ-agent
$env:ENV_FILE_PATH="d:\doc-summ-agent\config\.env"
$env:PYTHONPATH="d:\doc-summ-agent"
celery -A app.tasks.celery_tasks flower --port=5555
```

---

## ✅ After Starting Worker

1. **Upload a document** via API
2. **Watch worker terminal** - you should see processing messages
3. **Check document status** - should change to `completed`
4. **Verify results** - summary, QA results, chunks indexed

---

## 📝 What Gets Processed

When a document is processed, the worker:

1. ✅ Downloads file from storage
2. ✅ Loads document content
3. ✅ Generates summary using LLM (Gemini)
4. ✅ Answers questions (if provided)
5. ✅ Chunks document for RAG
6. ✅ Creates embeddings
7. ✅ Indexes in Chroma vector database
8. ✅ Updates MongoDB with results

---

## 🎯 Expected Results

After processing, a document should have:

- ✅ `status`: `"completed"`
- ✅ `summary`: Generated summary text
- ✅ `qa_results`: Question-answer pairs
- ✅ `chunks_indexed`: Number of chunks (e.g., 5)
- ✅ `vector_db_indexed`: `true`
- ✅ `processing_time`: Time taken in seconds
- ✅ `processed_at`: Timestamp

---

## 🚨 Important Notes

1. **Worker must be running** - Without it, tasks just sit in the queue
2. **Same Redis instance** - Worker and API must use same Redis
3. **Environment variables** - Worker needs same `.env` file
4. **Keep worker running** - Stop it and processing stops

---

## 💡 Production Setup

For production, you might want to:

1. **Run as service** - Use systemd (Linux) or Windows Service
2. **Multiple workers** - Scale horizontally
3. **Auto-restart** - Use supervisor or similar
4. **Monitoring** - Use Flower or Prometheus

---

## ✅ Summary

**The Problem:** Documents upload but don't get processed

**The Solution:** Start Celery worker to process queued tasks

**The Command:**
```powershell
celery -A app.tasks.celery_tasks worker --loglevel=info
```

**The Result:** Documents will be processed automatically when uploaded!

