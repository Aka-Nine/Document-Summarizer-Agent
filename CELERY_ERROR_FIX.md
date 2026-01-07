# Celery Task Error Fixes

**Status:** ✅ Fixed two errors in document processing

---

## 🐛 Errors Found

### Error 1: `NameError: name 'document' is not defined`
**Location:** `app/core/enterprise_document_processor.py:232`

**Problem:**
```python
summary_prompt = f"""Please provide a comprehensive summary of the following document:

{document}  # ❌ Variable 'document' doesn't exist

Summary:"""
```

**Fix:**
Changed `{document}` to `{full_text}` (the actual variable name).

```python
summary_prompt = f"""Please provide a comprehensive summary of the following document:

{full_text}  # ✅ Correct variable name

Summary:"""
```

---

### Error 2: `RuntimeWarning: coroutine 'ChromaVectorDBService.create_index' was never awaited`
**Location:** `app/core/rag_processor.py:35`

**Problem:**
`create_index()` is an async method but was being called from a synchronous `__init__` method without `await`.

**Fix:**
Added proper async handling to call the async method from sync context:

```python
def _ensure_index_exists(self):
    """Ensure vector index exists (called from sync context)"""
    try:
        dimension = self.embeddings_service.dimension
        # Handle async call from sync context
        try:
            loop = asyncio.get_running_loop()
            # Loop is running, schedule as background task
            asyncio.create_task(self.vector_db.create_index(dimension))
        except RuntimeError:
            # No running loop, try to get event loop
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    asyncio.create_task(self.vector_db.create_index(dimension))
                else:
                    loop.run_until_complete(self.vector_db.create_index(dimension))
            except RuntimeError:
                # No event loop at all, create new one
                asyncio.run(self.vector_db.create_index(dimension))
    except Exception as e:
        logger.warning("Index creation check failed", error=str(e))
```

---

## ✅ Changes Made

1. **Fixed variable name** in `_generate_summary()` method
2. **Fixed async/await** issue in `_ensure_index_exists()` method
3. **Added asyncio import** to `rag_processor.py`

---

## 🧪 Testing

After these fixes:

1. **Restart Celery worker** to pick up code changes:
   ```powershell
   # Stop worker (Ctrl+C)
   # Restart worker
   celery -A app.tasks.celery_tasks worker --loglevel=info --pool=solo
   ```

2. **Upload a test document** via API

3. **Check worker logs** - should see:
   - ✅ Document loaded
   - ✅ Document chunked
   - ✅ Vectors upserted
   - ✅ **Summary generated** (no more error!)
   - ✅ Document processing completed

---

## 📝 Files Modified

- `app/core/enterprise_document_processor.py` - Fixed variable name
- `app/core/rag_processor.py` - Fixed async call handling

---

## 🎯 Expected Behavior

After restarting the worker and uploading a document:

1. Document loads successfully ✅
2. Document is chunked ✅
3. Vectors are indexed in Chroma ✅
4. **Summary is generated** ✅ (was failing before)
5. Document status updates to "completed" ✅

