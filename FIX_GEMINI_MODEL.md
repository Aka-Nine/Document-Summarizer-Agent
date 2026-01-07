# Fix: Gemini Model 404 Error

**Error:** `404 models/gemini-1.5-flash is not found for API version v1beta`

**Root Cause:** `gemini-1.5-flash` is not available in the v1beta API that LangChain uses by default.

---

## ✅ Quick Fix

Update your `.env` file (not `config.env` - the actual `.env` file):

```env
# Change from:
GEMINI_MODEL=gemini-1.5-flash

# To one of these working options:
GEMINI_MODEL=gemini-pro                    # ✅ Recommended - stable, works with v1beta
# OR
GEMINI_MODEL=gemini-1.5-pro-001           # ✅ For 1.5 features (with version suffix)
```

---

## 🔍 Why This Happens

1. **LangChain uses v1beta API by default** - This API only supports:
   - `gemini-pro`
   - `gemini-pro-vision`

2. **Newer models (1.5, 2.0) require v1 API** - But LangChain's `ChatGoogleGenerativeAI` doesn't easily support switching API versions

3. **Model name format matters** - Some 1.5 models need `-001` or `-latest` suffix

---

## 📝 Solution Options

### Option 1: Use `gemini-pro` (Recommended)
```env
GEMINI_MODEL=gemini-pro
```
- ✅ Works immediately
- ✅ Stable and reliable
- ✅ Good for most use cases

### Option 2: Try `gemini-1.5-pro-001`
```env
GEMINI_MODEL=gemini-1.5-pro-001
```
- ⚠️ May or may not work depending on LangChain version
- ✅ If it works, gives you 1.5 features

### Option 3: Use Alternative Provider
If you need 1.5 features and Gemini doesn't work, switch to:
```env
LLM_PROVIDER=groq
GROQ_MODEL=llama3-8b-8192
```

---

## 🧪 After Changing Config

1. **Restart Celery worker:**
   ```powershell
   # Stop worker (Ctrl+C)
   # Restart
   celery -A app.tasks.celery_tasks worker --loglevel=info --pool=solo
   ```

2. **Test with a document upload** - should work now!

---

## 🔧 Code Changes Made

Added error handling to try alternative model name formats automatically, but **the best fix is to use a compatible model name in your config**.

---

## 📚 Valid Model Names

### ✅ Confirmed Working:
- `gemini-pro` - Stable, works with v1beta
- `gemini-pro-vision` - For image inputs

### ⚠️ May Work (depends on LangChain version):
- `gemini-1.5-pro-001`
- `gemini-1.5-flash-001`
- `gemini-1.5-pro-latest`

### ❌ Won't Work:
- `gemini-1.5-flash` (without suffix)
- `gemini-2.5-pro` (too new)

---

## 💡 Recommendation

**Use `gemini-pro` for now** - it's the most reliable option:

```env
GEMINI_MODEL=gemini-pro
```

This will work immediately and avoid API version issues.

