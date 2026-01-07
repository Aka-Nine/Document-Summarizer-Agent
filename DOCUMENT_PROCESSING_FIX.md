# Document Processing Issue - Solution

**Problem:** Documents are uploaded to MongoDB but not processed (no summaries, no vector indexing, no RAG)

**Root Cause:** Celery worker is not running to process queued tasks

---

## 🔍 What's Happening

When you upload a document:

1. ✅ **File is stored** in cloud storage (filesystem)
2. ✅ **Document record is created** in MongoDB with status `pending`
3. ✅ **Task is queued** in Redis via `process_document_task.delay()`
4. ❌ **Task is NOT processed** because Celery worker is not running

The task sits in the Redis queue waiting for a worker to pick it up.

---

## ✅ Solution: Start Celery Worker

### Quick Start (PowerShell)

**Option 1: Use the script**
```powershell
.\scripts\start_celery_worker.ps1
```

**Option 2: Manual start**
```powershell
cd d:\doc-summ-agent
$env:ENV_FILE_PATH="d:\doc-summ-agent\config\.env"
$env:PYTHONPATH="d:\doc-summ-agent"
celery -A app.tasks.celery_tasks worker --loglevel=info
```

---

## 📋 What the Worker Does

Once the Celery worker is running, it will:

1. **Pick up tasks** from Redis queue
2. **Download file** from cloud storage
3. **Process document** with EnterpriseDocumentProcessor:
   - Load document content
   - Generate summary using Gemini LLM
   - Answer questions (if provided)
   - Chunk document for RAG
   - Create embeddings
   - Index in Chroma vector database
4. **Update MongoDB** with:
   - Summary
   - QA results
   - Processing status (`completed`)
   - Chunks indexed count
   - Processing time

---

## 🎯 Expected Results

After starting the worker and uploading a document:

### Before (Worker Not Running)
```json
{
  "status": "pending",
  "summary": null,
  "qa_results": null,
  "chunks_indexed": 0,
  "vector_db_indexed": false
}
```

### After (Worker Running)
```json
{
  "status": "completed",
  "summary": "This document discusses...",
  "qa_results": {
    "What is this about?": "This document is about..."
  },
  "chunks_indexed": 5,
  "vector_db_indexed": true,
  "processing_time": 12.5,
  "processed_at": "2026-01-04T20:00:00Z"
}
```

---

## 🔄 Complete Setup

### Terminal 1: API Server
```powershell
cd d:\doc-summ-agent
$env:ENV_FILE_PATH="d:\doc-summ-agent\config\.env"
$env:PYTHONPATH="d:\doc-summ-agent"
python run.py
```
**Keep this running** - This serves the API

### Terminal 2: Celery Worker
```powershell
cd d:\doc-summ-agent
$env:ENV_FILE_PATH="d:\doc-summ-agent\config\.env"
$env:PYTHONPATH="d:\doc-summ-agent"
celery -A app.tasks.celery_tasks worker --loglevel=info
```
**Keep this running** - This processes documents

---

## ✅ Verification Steps

### 1. Check Worker is Running
You should see in the worker terminal:
```
[tasks]
  . app.tasks.celery_tasks.process_document_task
  . app.tasks.celery_tasks.query_document_task

celery@hostname ready.
```

### 2. Upload a Document
```bash
POST /api/v1/documents/upload
```

### 3. Watch Worker Logs
You should see:
```
[INFO] Received task: process_document_task[abc123...]
[INFO] Document processing started
[INFO] File downloaded from cloud storage
[INFO] Document processing completed
```

### 4. Check Document Status
```bash
GET /api/v1/documents/{document_id}
```
Status should be `completed` with summary and results.

---

## 🛠️ Troubleshooting

### Worker won't start
- **Check Redis connection**: `python -c "from app.services.redis_service import RedisService; RedisService()"`
- **Check environment variables**: Make sure `ENV_FILE_PATH` and `PYTHONPATH` are set
- **Check dependencies**: `pip install -r config/requirements.txt`

### Tasks queued but not processing
- **Verify worker is running**: Check worker terminal for activity
- **Check Redis connection**: Worker and API must use same Redis
- **Check worker logs**: Look for error messages

### Processing fails
- **Check LLM API keys**: Gemini API key must be valid
- **Check quota**: Make sure you haven't exceeded API limits
- **Check logs**: Worker logs will show specific errors

---

## 📊 Monitoring

### Option 1: Worker Logs
Watch the terminal where worker is running - all processing is logged there.

### Option 2: Flower (Web UI)
```powershell
celery -A app.tasks.celery_tasks flower --port=5555
```
Visit: http://localhost:5555

### Option 3: API Endpoints
- `GET /api/v1/documents` - List all documents with status
- `GET /api/v1/documents/{id}` - Check specific document status

---

## 🎯 Summary

**The Issue:** Documents upload but don't get processed

**The Cause:** Celery worker not running

**The Fix:** Start Celery worker in a separate terminal

**The Command:**
```powershell
celery -A app.tasks.celery_tasks worker --loglevel=info
```

**The Result:** Documents will be automatically processed when uploaded!

---

## 📝 Files Created

1. **START_CELERY_WORKER.md** - Detailed guide for starting workers
2. **scripts/start_celery_worker.ps1** - PowerShell script to start worker
3. **DOCUMENT_PROCESSING_FIX.md** - This file (summary of issue and solution)

---

## ✅ Next Steps

1. **Start the Celery worker** using the command above
2. **Upload a test document** via API
3. **Watch the worker process it** in real-time
4. **Check the results** via API endpoint
5. **Enjoy automatic document processing!** 🎉

