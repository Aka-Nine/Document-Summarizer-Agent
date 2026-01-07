# docx2txt Module Not Found - Fix

**Error:** `No module named 'docx2txt'`

**Status:** Module is installed but worker may need restart

---

## ✅ Solution

### Step 1: Verify Installation
```powershell
pip install docx2txt>=0.8
```

### Step 2: Restart Celery Worker
The worker must be restarted to pick up the installed module:

```powershell
# Stop current worker (Ctrl+C)

# Restart with correct pool
cd d:\doc-summ-agent
$env:ENV_FILE_PATH="d:\doc-summ-agent\config\.env"
$env:PYTHONPATH="d:\doc-summ-agent"
python -c "from dotenv import load_dotenv; load_dotenv('config/.env', override=True)"
celery -A app.tasks.celery_tasks worker --loglevel=info --pool=solo
```

### Step 3: Verify Import
After restarting, the worker should be able to import `docx2txt`.

---

## 🔍 Why This Happens

1. **Module installed after worker started** - Worker needs restart
2. **Different Python environment** - Worker using different Python than where module was installed
3. **Path issues** - PYTHONPATH not set correctly for worker

---

## ✅ Verification

After restarting the worker, upload a `.docx` file. The task should:
1. ✅ Pick up the task
2. ✅ Load the document using `Docx2txtLoader`
3. ✅ Process successfully

---

## 📝 Code Changes

Added better error handling in `app/core/enterprise_document_processor.py`:
- Checks if `docx2txt` is available before using `Docx2txtLoader`
- Provides clear error message if module is missing

---

## 🚨 If Still Failing

If the error persists after restarting:

1. **Check Python environment:**
   ```powershell
   python -c "import sys; print(sys.executable)"
   ```

2. **Verify module in same environment:**
   ```powershell
   python -c "import docx2txt; print('OK')"
   ```

3. **Reinstall module:**
   ```powershell
   pip uninstall docx2txt -y
   pip install docx2txt>=0.8
   ```

4. **Check requirements:**
   ```powershell
   pip install -r config/requirements.txt
   ```

