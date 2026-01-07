# Celery Task Fix - MongoDB Document Access

**Error:** `'dict' object has no attribute 'filename'`

**Root Cause:** MongoDB documents are dictionaries, not objects. Code was using attribute access (`.filename`) instead of dictionary access (`['filename']` or `.get('filename')`)

**Solution:** Changed attribute access to dictionary access

---

## ✅ Fixed

### **File:** `app/tasks/celery_tasks.py`

**Before (Incorrect):**
```python
metadata = {
    "filename": doc.filename,      # ❌ Attribute access
    "file_type": doc.file_type,     # ❌ Attribute access
    "user_id": doc.user_id,         # ❌ Attribute access
    "document_id": document_id
}
```

**After (Correct):**
```python
metadata = {
    "filename": doc.get("filename", ""),      # ✅ Dictionary access
    "file_type": doc.get("file_type", ""),   # ✅ Dictionary access
    "user_id": doc.get("user_id", ""),       # ✅ Dictionary access
    "document_id": document_id
}
```

---

## 🔍 Why This Happens

MongoDB's `find_one()` returns a **dictionary**, not an object:

```python
doc = documents_collection.find_one({"_id": doc_id_obj})
# doc is a dict: {"_id": ObjectId(...), "filename": "...", ...}
# NOT an object with attributes
```

**Correct Access:**
- ✅ `doc["filename"]` - Direct key access
- ✅ `doc.get("filename", "")` - Safe access with default
- ❌ `doc.filename` - Attribute access (doesn't work on dicts)

---

## ✅ Verification

The fix ensures:
1. ✅ Dictionary access is used consistently
2. ✅ Default values provided for missing fields
3. ✅ No more attribute errors

---

## 🧪 Test It

1. **Restart Celery worker** (if running)
2. **Upload a document** via API
3. **Watch worker process it** - Should work without errors!

---

## 📝 Summary

**The Problem:** Using attribute access on MongoDB dict

**The Fix:** Changed to dictionary access with `.get()`

**The Result:** Tasks process documents without attribute errors!

