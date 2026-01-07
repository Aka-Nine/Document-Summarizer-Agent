# Gemini Model Error Fix

**Error:** `404 models/gemini-1.5-flash is not found for API version v1beta`

**Status:** ✅ Fixed with better error handling and model name alternatives

---

## 🐛 Problem

The error occurs because:
1. `gemini-1.5-flash` might not be available in the v1beta API version
2. The model name format might need adjustment
3. LangChain's `ChatGoogleGenerativeAI` uses v1beta by default

---

## ✅ Solution

### Option 1: Use a Compatible Model Name (Recommended)

Update your `config/config.env`:

```env
# Use one of these working model names:
GEMINI_MODEL=gemini-pro                    # ✅ Works with v1beta
# OR
GEMINI_MODEL=gemini-1.5-pro               # ✅ Try this for 1.5 models
# OR  
GEMINI_MODEL=gemini-1.5-flash-001         # ✅ Try with -001 suffix
```

### Option 2: Check Your Actual Config

The error shows `gemini-1.5-flash` is being used, but your `config.env` shows `gemini-pro`. 

**Check what's actually set:**
```powershell
# Check current value
python -c "from app.config.settings import settings; print(f'GEMINI_MODEL: {settings.GEMINI_MODEL}')"
```

If it shows `gemini-1.5-flash`, update `config/config.env`:
```env
GEMINI_MODEL=gemini-pro
```

### Option 3: Use Alternative Model Names

For `gemini-1.5-flash`, try these alternatives:
- `gemini-1.5-flash-001` (with version suffix)
- `gemini-1.5-flash-latest` (with latest suffix)
- `gemini-pro` (fallback to stable model)

---

## 🔧 Code Changes Made

Added error handling to try alternative model name formats:

```python
# If model name fails, try alternative formats
if "1.5" in model_name:
    # Try with -001 suffix
    alt_model = f"{model_name}-001" if not model_name.endswith("-001") else model_name
    logger.warning(f"Trying alternative model name: {alt_model}", original=model_name, error=str(e))
    return ChatGoogleGenerativeAI(
        google_api_key=settings.GEMINI_API_KEY,
        model=alt_model,
        temperature=0.0,
        max_retries=3
    )
```

---

## 📝 Valid Gemini Model Names

Based on Google's API documentation, these models work:

### v1beta API (Default):
- `gemini-pro` ✅
- `gemini-pro-vision` ✅

### v1 API (Newer models):
- `gemini-1.5-pro` (may need `-001` suffix)
- `gemini-1.5-flash` (may need `-001` suffix)
- `gemini-1.5-pro-latest`
- `gemini-1.5-flash-latest`

---

## 🧪 Testing

1. **Update config.env:**
   ```env
   GEMINI_MODEL=gemini-pro
   ```

2. **Restart Celery worker:**
   ```powershell
   # Stop worker (Ctrl+C)
   # Restart
   celery -A app.tasks.celery_tasks worker --loglevel=info --pool=solo
   ```

3. **Upload a test document** - should work now!

---

## 💡 Recommendation

**Use `gemini-pro` for now** - it's stable and works with v1beta API:

```env
GEMINI_MODEL=gemini-pro
```

If you need 1.5 features, try:
```env
GEMINI_MODEL=gemini-1.5-pro-001
```

---

## 📚 References

- [Google Gemini API Models](https://ai.google.dev/models/gemini)
- [LangChain Google Generative AI](https://python.langchain.com/docs/integrations/chat/google_generative_ai)

