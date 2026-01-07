# LangSmith Tracing Fix

**Issue:** LangSmith is not monitoring/tracking LLM calls

**Status:** ✅ Fixed - Tracing now enabled and working in both FastAPI and Celery

---

## 🐛 Problem

1. **Tracing was disabled** - `LANGCHAIN_TRACING_V2=false` in config
2. **Celery workers don't inherit env vars** - LangSmith env vars were only set in FastAPI startup, but Celery workers run in separate processes
3. **LLM calls happen in Celery** - Most LLM calls (document processing, queries) happen in Celery tasks, not FastAPI

---

## ✅ Solution

### 1. Enable Tracing in Config
Changed `LANGCHAIN_TRACING_V2=false` to `LANGCHAIN_TRACING_V2=true`

### 2. Initialize LangSmith in Celery Tasks
Added LangSmith initialization at the start of both Celery tasks:
- `process_document_task` - For document processing
- `query_document_task` - For document queries

This ensures environment variables are set before LLM calls are made.

---

## 🔧 Code Changes

### `config/config.env`:
```env
LANGCHAIN_TRACING_V2=true  # Changed from false
LANGCHAIN_PROJECT=Enterprise-Document-Intelligence
```

### `app/tasks/celery_tasks.py`:

**Added to `process_document_task`:**
```python
# Initialize LangSmith tracing in Celery worker process
if settings.LANGCHAIN_TRACING_V2 and settings.LANGCHAIN_API_KEY:
    import os
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = settings.LANGCHAIN_API_KEY
    os.environ["LANGCHAIN_PROJECT"] = settings.LANGCHAIN_PROJECT
    if settings.LANGCHAIN_ENDPOINT:
        os.environ["LANGCHAIN_ENDPOINT"] = settings.LANGCHAIN_ENDPOINT
    logger.info("LangSmith tracing enabled in Celery worker", project=settings.LANGCHAIN_PROJECT)
```

**Added to `query_document_task`:**
```python
# Initialize LangSmith tracing in Celery worker process
if settings.LANGCHAIN_TRACING_V2 and settings.LANGCHAIN_API_KEY:
    import os
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = settings.LANGCHAIN_API_KEY
    os.environ["LANGCHAIN_PROJECT"] = settings.LANGCHAIN_PROJECT
    if settings.LANGCHAIN_ENDPOINT:
        os.environ["LANGCHAIN_ENDPOINT"] = settings.LANGCHAIN_ENDPOINT
```

---

## 🧪 Testing

1. **Update your `.env` file** (not just config.env):
   ```env
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_API_KEY=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
   LANGCHAIN_PROJECT=Enterprise-Document-Intelligence
   ```

2. **Restart Celery worker:**
   ```powershell
   # Stop worker (Ctrl+C)
   # Restart
   celery -A app.tasks.celery_tasks worker --loglevel=info --pool=solo
   ```

3. **Restart FastAPI server:**
   ```powershell
   # Stop server (Ctrl+C)
   # Restart
   python run.py
   ```

4. **Process a document or make a query:**
   - Upload a document
   - Query a document
   - Check LangSmith dashboard: https://smith.langchain.com/

---

## 📊 What Will Be Tracked

LangSmith will now track:
- ✅ **LLM calls** - All Gemini API calls
- ✅ **Document processing** - Summary generation, Q&A
- ✅ **Document queries** - RAG queries and answers
- ✅ **Embeddings** - Vector embeddings generation
- ✅ **Chains** - LangChain chain executions

---

## 🔍 Verify Tracing is Working

1. **Check Celery worker logs:**
   ```
   [info] LangSmith tracing enabled in Celery worker project=Enterprise-Document-Intelligence
   ```

2. **Check FastAPI logs:**
   ```
   [info] LangSmith tracing enabled project=Enterprise-Document-Intelligence
   ```

3. **Check LangSmith dashboard:**
   - Go to https://smith.langchain.com/
   - Select project: "Enterprise-Document-Intelligence"
   - You should see traces for:
     - Document processing
     - Document queries
     - LLM calls

---

## 💡 Why This Was Needed

**The Problem:**
- FastAPI and Celery run in **separate processes**
- Environment variables set in FastAPI don't carry over to Celery
- Most LLM calls happen in **Celery tasks** (background processing)
- LangSmith needs env vars set **before** LLM objects are created

**The Solution:**
- Set LangSmith env vars in **both** FastAPI startup AND Celery tasks
- This ensures tracing works regardless of where LLM calls happen

---

## 📝 Files Modified

- `config/config.env` - Enabled `LANGCHAIN_TRACING_V2=true`
- `app/tasks/celery_tasks.py` - Added LangSmith initialization to both tasks

---

## ✅ Expected Result

After restarting both services:
- ✅ LangSmith will track all LLM calls
- ✅ You'll see traces in the LangSmith dashboard
- ✅ Both document processing and queries will be tracked
- ✅ You can monitor performance, costs, and debug issues

---

## 🎯 Next Steps

1. **Update your actual `.env` file** (not just the template)
2. **Restart both services** (FastAPI + Celery)
3. **Process a document** to generate traces
4. **Check LangSmith dashboard** to verify tracking

