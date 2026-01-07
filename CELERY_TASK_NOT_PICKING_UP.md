# Celery Tasks Not Being Picked Up - Troubleshooting

**Issue:** Tasks are queued but worker is not picking them up

**Diagnosis:** Worker is running but using wrong pool type or tasks are failing

---

## 🔍 Diagnostic Results

From the diagnostics, I found:

1. ✅ **Worker is running** - `celery@Nine` is active
2. ✅ **Tasks are being queued** - Found in Redis
3. ❌ **Worker using wrong pool** - Using `prefork` instead of `solo` on Windows
4. ❌ **Tasks are failing** - Recent tasks show `FAILURE` status

---

## ✅ Solutions

### Issue 1: Worker Using Wrong Pool

**Problem:** Worker shows `Pool: celery.concurrency.prefork:TaskPool`  
**Solution:** Worker must be started with `--pool=solo` on Windows

**Correct Command:**
```powershell
cd d:\doc-summ-agent
$env:ENV_FILE_PATH="d:\doc-summ-agent\config\.env"
$env:PYTHONPATH="d:\doc-summ-agent"
python -c "from dotenv import load_dotenv; load_dotenv('config/.env', override=True)"
celery -A app.tasks.celery_tasks worker --loglevel=info --pool=solo
```

**Important:** The `--pool=solo` flag is required!

### Issue 2: Tasks Failing

**Problem:** Tasks are being picked up but failing immediately  
**Solution:** Check worker logs for specific error messages

**Check Worker Logs:**
- Look for error messages in the worker terminal
- Common errors:
  - Attribute errors (fixed)
  - Import errors
  - Configuration errors

### Issue 3: Redis URL Format

**Fixed:** Updated Redis URL generation to use `redis://` instead of `rediss://`

---

## 🧪 Verify Worker is Correctly Configured

### Step 1: Stop Current Worker
Press `Ctrl+C` in the worker terminal

### Step 2: Start Worker with Correct Pool
```powershell
celery -A app.tasks.celery_tasks worker --loglevel=info --pool=solo
```

### Step 3: Verify Pool Type
You should see in worker output:
```
[pool: solo]
```

NOT:
```
[pool: prefork]  ❌ Wrong for Windows
```

### Step 4: Test Task Queuing
Upload a document via API and watch worker terminal for:
```
[INFO] Task process_document_task[...] received
[INFO] Document processing started
```

---

## 🔍 Check Task Status

Run the diagnostic script:
```powershell
python check_celery_tasks.py
```

Look for:
- **Active tasks:** Should show tasks being processed
- **Reserved tasks:** Should show queued tasks waiting
- **Task results:** Check if tasks are SUCCESS or FAILURE

---

## 🚨 Common Issues

### Issue: "DuplicateNodenameWarning"
**Cause:** Multiple workers with same name  
**Fix:** Use unique worker names:
```powershell
celery -A app.tasks.celery_tasks worker --loglevel=info --pool=solo -n worker1@%h
```

### Issue: Tasks Queued but Not Processing
**Causes:**
1. Worker not running
2. Worker using wrong pool (prefork on Windows)
3. Worker not connected to same Redis
4. Tasks failing immediately

**Fix:** 
1. Restart worker with `--pool=solo`
2. Check worker logs for errors
3. Verify Redis connection

### Issue: Tasks Failing Immediately
**Causes:**
1. Code errors in task
2. Missing dependencies
3. Configuration errors

**Fix:**
1. Check worker logs for error messages
2. Test task function directly
3. Verify all dependencies installed

---

## ✅ Verification Checklist

- [ ] Worker is running
- [ ] Worker using `--pool=solo` (Windows)
- [ ] Worker connected to same Redis as API
- [ ] Tasks are being queued (check Redis)
- [ ] Tasks are being picked up (check worker logs)
- [ ] Tasks are completing successfully (not failing)

---

## 📝 Quick Fix Command

**Stop current worker and restart correctly:**

```powershell
# Stop worker (Ctrl+C)

# Start with correct pool
cd d:\doc-summ-agent
$env:ENV_FILE_PATH="d:\doc-summ-agent\config\.env"
$env:PYTHONPATH="d:\doc-summ-agent"
python -c "from dotenv import load_dotenv; load_dotenv('config/.env', override=True)"
celery -A app.tasks.celery_tasks worker --loglevel=info --pool=solo
```

---

## 🔄 Expected Behavior

**When Working Correctly:**

1. **Upload document** → API queues task
2. **Worker picks up task** → See in worker logs: `Task received`
3. **Task processes** → See: `Document processing started`
4. **Task completes** → See: `Document processing completed`
5. **MongoDB updated** → Document status changes to `completed`

**Watch for:**
- Task received messages
- Processing started messages
- Processing completed messages
- No error messages

---

## ✅ Summary

**The Problem:** Worker using wrong pool type or tasks failing

**The Fix:** 
1. Restart worker with `--pool=solo`
2. Check worker logs for errors
3. Verify Redis connection

**The Command:**
```powershell
celery -A app.tasks.celery_tasks worker --loglevel=info --pool=solo
```

