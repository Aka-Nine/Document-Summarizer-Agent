# Celery Worker Not Picking Up Tasks - Fix

**Status:** ✅ Tasks are registered correctly, but **worker is not running**

---

## 🔍 Diagnosis Results

The diagnostic script shows:
- ✅ Redis connection: Working
- ✅ Tasks registered: `process_document_task`, `query_document_task`
- ✅ Task import: Successful
- ❌ **No active workers found** - This is the problem!

---

## ✅ Solution: Start the Celery Worker

The Celery worker must be running to pick up tasks from the queue.

### Option 1: Using PowerShell Script (Recommended for Windows)

```powershell
cd d:\doc-summ-agent
.\scripts\start_celery_worker.ps1
```

### Option 2: Manual Start (Windows)

```powershell
cd d:\doc-summ-agent
$env:ENV_FILE_PATH="d:\doc-summ-agent\config\.env"
$env:PYTHONPATH="d:\doc-summ-agent"
python -c "from dotenv import load_dotenv; load_dotenv('config/.env', override=True)"
celery -A app.tasks.celery_tasks worker --loglevel=info --pool=solo
```

### Option 3: Using Python Script

```powershell
cd d:\doc-summ-agent
$env:ENV_FILE_PATH="d:\doc-summ-agent\config\.env"
$env:PYTHONPATH="d:\doc-summ-agent"
python scripts/celery_worker.py
```

---

## 🔍 Verify Worker is Running

After starting the worker, you should see output like:

```
[2026-01-07 21:31:19,567: INFO/MainProcess] Connected to redis://default:***@redis-17483.c261.us-east-1-4.ec2.cloud.redislabs.com:17483//
[2026-01-07 21:31:19,567: INFO/MainProcess] mingle: searching for neighbors
[2026-01-07 21:31:19,567: INFO/MainProcess] mingle: all alone
[2026-01-07 21:31:19,567: INFO/MainProcess] celery@HOSTNAME ready.
```

You should also see:
```
[tasks]
  . process_document_task
  . query_document_task
```

---

## 🧪 Test Task Processing

1. **Start the worker** (using one of the methods above)

2. **Upload a document** via the API:
   ```bash
   curl -X POST "http://localhost:8000/api/v1/documents/upload" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -F "file=@test.pdf"
   ```

3. **Check worker logs** - You should see:
   ```
   [INFO] Task process_document_task[xxx] received
   [INFO] Processing document: xxx
   ```

4. **Check task status** in MongoDB:
   ```javascript
   db.documents.findOne({_id: ObjectId("xxx")})
   // status should change from "pending" -> "processing" -> "completed"
   ```

---

## 🐛 Troubleshooting

### Issue: Worker starts but doesn't pick up tasks

**Check:**
1. **Same broker URL**: Worker and API must use the same Redis instance
   ```python
   # Check in worker logs:
   Connected to redis://...
   
   # Should match the broker URL in your .env
   ```

2. **Task name matches**: The task name in the API call must match the registered name
   ```python
   # In routes_mongodb.py:
   process_document_task.delay(document_id, question_list)
   
   # Should match the task name:
   @celery_app.task(name="process_document_task", ...)
   ```

3. **Worker pool type**: On Windows, must use `--pool=solo`
   ```powershell
   celery -A app.tasks.celery_tasks worker --pool=solo
   ```

### Issue: Tasks queued but not executing

**Check worker logs for errors:**
- Import errors
- Configuration errors
- Redis connection errors

**Check Redis for queued tasks:**
```python
import redis
r = redis.Redis(host='...', port=..., password='...')
# Check for tasks in queue
keys = r.keys("celery*")
print(keys)
```

### Issue: Worker crashes immediately

**Common causes:**
1. **Missing dependencies**: Install all requirements
   ```powershell
   pip install -r requirements.txt
   ```

2. **Environment variables not loaded**: Ensure `.env` is loaded
   ```powershell
   $env:ENV_FILE_PATH="d:\doc-summ-agent\config\.env"
   ```

3. **Python path issues**: Set PYTHONPATH
   ```powershell
   $env:PYTHONPATH="d:\doc-summ-agent"
   ```

---

## 📊 Monitor Worker Status

### Check active workers:
```powershell
celery -A app.tasks.celery_tasks inspect active
```

### Check registered tasks:
```powershell
celery -A app.tasks.celery_tasks inspect registered
```

### Check scheduled tasks:
```powershell
celery -A app.tasks.celery_tasks inspect scheduled
```

### Check worker stats:
```powershell
celery -A app.tasks.celery_tasks inspect stats
```

---

## ✅ Verification Checklist

- [ ] Worker is running (check process list or logs)
- [ ] Worker connected to Redis (check logs for "Connected to redis://...")
- [ ] Tasks are registered (check logs for task list)
- [ ] Worker pool is `solo` on Windows
- [ ] Environment variables loaded correctly
- [ ] Redis connection is working
- [ ] Tasks can be queued (check API response)
- [ ] Tasks are being picked up (check worker logs)

---

## 🔧 Code Changes Made

1. **Added explicit task inclusion** in `celery_tasks.py`:
   ```python
   celery_app.conf.update(
       # ...
       include=['app.tasks.celery_tasks'],
       autodiscover_tasks=False,
   )
   ```

2. **Fixed variable initialization** to prevent `name 'document' is not defined` errors

---

## 📝 Next Steps

1. **Start the worker** using one of the methods above
2. **Upload a test document** via the API
3. **Monitor worker logs** to see task execution
4. **Check MongoDB** to verify document status updates

---

## 💡 Tips

- **Keep worker running**: The worker must stay running to process tasks
- **Separate terminal**: Run worker in a separate terminal/process
- **Logs**: Check worker logs for detailed error messages
- **Restart after code changes**: Restart worker after modifying task code

