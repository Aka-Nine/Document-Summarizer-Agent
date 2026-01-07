# Frontend Document Display Fix

**Issue:** Frontend not able to see processed files

**Status:** ✅ Fixed - API now returns required fields

---

## 🐛 Problem

The frontend was not displaying processed documents because the API's `list_documents` endpoint was missing two critical fields:

1. **`summary`** - Used to display document summary in the document list
2. **`vector_db_indexed`** - Used to filter completed documents that are ready for querying

---

## ✅ Solution

Updated the `list_documents` endpoint in `app/api/v1/routes_mongodb.py` to include:

```python
return [
    {
        "id": str(doc["_id"]),
        "filename": doc.get("filename"),
        "status": doc.get("status"),
        "file_type": doc.get("file_type"),
        "file_size": doc.get("file_size"),
        "summary": doc.get("summary"),  # ✅ Added
        "rag_enabled": doc.get("rag_enabled", True),
        "chunks_indexed": doc.get("chunks_indexed", 0),
        "vector_db_indexed": doc.get("vector_db_indexed", False),  # ✅ Added
        "created_at": doc.get("created_at").isoformat() if doc.get("created_at") else None,
        "processed_at": doc.get("processed_at").isoformat() if doc.get("processed_at") else None,
        "processing_time": doc.get("processing_time"),
        "updated_at": doc.get("updated_at").isoformat() if doc.get("updated_at") else None
    }
    for doc in documents
]
```

---

## 📋 What Was Missing

### Before:
- ❌ No `summary` field - Frontend couldn't display document summaries
- ❌ No `vector_db_indexed` field - Frontend couldn't filter queryable documents

### After:
- ✅ `summary` included - Frontend can now display summaries
- ✅ `vector_db_indexed` included - Frontend can filter completed documents

---

## 🎯 Frontend Usage

### DocumentList Component:
- Uses `summary` to display document preview (line 158-162)
- Uses `status` to show processing status
- Uses `chunks_indexed` to show indexing info

### DocumentQuery Component:
- Filters documents by `status === 'completed' && vector_db_indexed` (line 51-52)
- Only shows documents that are fully processed and indexed

---

## 🧪 Testing

1. **Restart the FastAPI server** (if needed):
   ```powershell
   # Stop server (Ctrl+C)
   # Restart
   python run.py
   ```

2. **Check the frontend:**
   - Upload a document
   - Wait for processing to complete
   - Check document list - should now show:
     - ✅ Summary text
     - ✅ Status badge
     - ✅ "View & Query" button (for completed documents)

3. **Check document query page:**
   - Should show completed documents in the dropdown
   - Only documents with `vector_db_indexed: true` will appear

---

## 📝 Files Modified

- `app/api/v1/routes_mongodb.py` - Added `summary` and `vector_db_indexed` to list response

---

## ✅ Expected Behavior

After this fix:

1. **Document List Page:**
   - ✅ Shows all uploaded documents
   - ✅ Displays summary for completed documents
   - ✅ Shows status badges (pending, processing, completed, failed)
   - ✅ Shows "View & Query" button for completed documents

2. **Document Query Page:**
   - ✅ Shows only completed and indexed documents
   - ✅ Allows querying processed documents
   - ✅ Filters out incomplete documents

---

## 💡 Additional Notes

- The `summary` field is populated during document processing
- The `vector_db_indexed` field is set to `true` when chunks are successfully indexed in Chroma
- Documents with `status: 'completed'` and `vector_db_indexed: true` are ready for querying

