# "name 'document' is not defined" - Fix

**Error:** `name 'document' is not defined`

**Status:** Fixed exception handler variable scope issues

---

## ✅ Solution

### Problem
The exception handler was trying to use variables (`documents_collection`, `doc_id_obj`) that might not be defined if an exception occurred early in the function.

### Fix Applied

1. **Initialize variables at function start:**
   - `documents_collection = None`
   - `doc_id_obj = None`
   - `doc = None`

2. **Improved exception handler:**
   - Check if variables are `None` before using them
   - Better error handling for update failures

---

## 🔍 Code Changes

### Before:
```python
temp_file_path = None

try:
    documents_collection = get_documents_collection()
    # ... rest of code
except Exception as e:
    if 'doc_id_obj' in locals():  # ❌ Might fail if documents_collection not defined
        documents_collection.update_one(...)  # ❌ documents_collection might not exist
```

### After:
```python
temp_file_path = None
documents_collection = None
doc_id_obj = None
doc = None

try:
    documents_collection = get_documents_collection()
    # ... rest of code
except Exception as e:
    if documents_collection is not None and doc_id_obj is not None:  # ✅ Safe check
        try:
            documents_collection.update_one(...)  # ✅ Safe to use
        except Exception as update_error:
            logger.warning("Failed to update document status", error=str(update_error))
```

---

## ✅ Verification

After this fix:
1. ✅ Variables are always defined (initialized to `None`)
2. ✅ Exception handler safely checks for `None` before use
3. ✅ Better error logging for update failures

---

## 🚨 If Error Persists

If you still see `name 'document' is not defined`:

1. **Check the full traceback** - The error might be from a different location
2. **Restart Celery worker** - Changes require worker restart:
   ```powershell
   # Stop worker (Ctrl+C)
   # Restart worker
   celery -A app.tasks.celery_tasks worker --loglevel=info --pool=solo
   ```
3. **Check for typos** - Look for any references to `document` instead of `doc` or `documents_collection`

---

## 📝 Related Files

- `app/tasks/celery_tasks.py` - Main task file (fixed)


