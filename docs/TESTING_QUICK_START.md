# API Testing - Quick Start Guide

## 🎯 What You Have

I've created **5 complete testing tools** for you:

### 1. **Swagger UI** (Easiest) 🌐
- Built-in interactive interface
- No installation needed
- Access: `http://localhost:8000/docs`
- **Best for**: Quick testing, exploring endpoints

### 2. **test_api.py** (Automated) 🐍
- Comprehensive Python test suite
- Tests all major endpoints
- 5 test classes with 9+ test methods
- File: `test_api.py` (14.7 KB)
- **Best for**: Automated testing, CI/CD, validation

### 3. **API_TESTING_WITH_CURL.sh** (Command Line) 💻
- Shell script with cURL examples
- Copy-paste ready commands
- Works on Mac/Linux/Windows (with curl)
- File: `API_TESTING_WITH_CURL.sh` (6.2 KB)
- **Best for**: Quick CLI testing, shell automation

### 4. **API_Testing_PowerShell.ps1** (Windows) 🪟
- PowerShell script for Windows users
- 9 individual test functions
- Can run all tests or specific ones
- File: `API_Testing_PowerShell.ps1` (16.3 KB)
- **Best for**: Windows users, native PowerShell

### 5. **Postman_Collection.json** (Desktop App) 📮
- Import into Postman application
- Pre-configured endpoints
- Auto-save tokens and IDs
- File: `Postman_Collection.json` (9.4 KB)
- **Best for**: Visual testing, team collaboration

### 6. **API_TESTING_GUIDE.md** (Documentation) 📖
- Complete testing guide
- Examples for all 4 methods
- Troubleshooting section
- File: `API_TESTING_GUIDE.md` (13.3 KB)
- **Best for**: Learning, reference

---

## 🚀 Quick Start (Choose One)

### Option A: Swagger UI (Recommended for beginners)

```bash
# 1. Start the API
python run.py

# 2. Open browser
http://localhost:8000/docs

# 3. Click "Try it out" on any endpoint
# 4. Click "Execute"
# 5. See the response!
```

**Advantages:**
- No coding required
- Visual interface
- Immediate feedback
- Built-in documentation

---

### Option B: Python Script

```bash
# 1. Start the API
python run.py

# 2. In another terminal, run tests
python test_api.py

# 3. Watch the test suite execute all tests
# 4. See results in console
```

**Advantages:**
- Automated testing
- Detailed output
- Can integrate with CI/CD
- Repeatable

---

### Option C: PowerShell (Windows)

```powershell
# 1. Start the API
python run.py

# 2. In another PowerShell, source the script
. .\API_Testing_PowerShell.ps1

# 3. Run tests
Run-AllTests

# Or run individual tests:
Test-HealthCheck
Test-UserLogin
Test-DocumentUpload
```

**Advantages:**
- Native Windows integration
- Colored output
- Easy to customize
- Interactive

---

### Option D: cURL (Command Line)

```bash
# 1. Start the API
python run.py

# 2. Test health
curl http://localhost:8000/health

# 3. Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user@example.com","password":"pass"}'

# 4. Copy token from response and use in subsequent requests
TOKEN="your_token_here"
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/documents
```

**Advantages:**
- Lightweight
- Works everywhere
- Full control
- Scriptable

---

### Option E: Postman (Desktop)

```
1. Download Postman: https://www.postman.com/downloads/
2. Open Postman
3. Click "Import"
4. Select "Postman_Collection.json"
5. Test endpoints with pre-configured requests
```

**Advantages:**
- Beautiful UI
- Environment variables
- Request history
- Team features
- Can create workflows

---

## 📋 What Each Test Does

### Health Check
Verifies API is running and all services are connected.

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "redis": "connected",
  "vector_db": "connected"
}
```

### User Registration
Creates a new user account.

**Input:**
```json
{
  "username": "user@example.com",
  "password": "Password123!",
  "full_name": "User Name"
}
```

### User Login
Authenticates user and returns JWT token.

**Response:**
```json
{
  "access_token": "eyJ0eXAi...",
  "token_type": "bearer"
}
```

### Document Upload
Uploads a file for processing (PDF, DOCX, TXT, MD).

**Response:**
```json
{
  "document_id": "uuid-here",
  "title": "My Document",
  "status": "processing",
  "created_at": "2025-12-01T..."
}
```

### Search
Performs semantic search across documents.

**Query:** `?q=search_term&top_k=5`

**Response:**
```json
{
  "results": [
    {
      "document_id": "uuid",
      "text": "Relevant chunk...",
      "score": 0.95
    }
  ]
}
```

### Chat (RAG)
Asks questions about documents with context retrieval.

**Input:**
```json
{
  "message": "What is this about?",
  "document_id": "uuid"
}
```

**Response:**
```json
{
  "response": "This document is about...",
  "sources": [
    {"text": "Source chunk...", "score": 0.92}
  ]
}
```

### Summarize
Generates a summary of the document.

**Input:**
```json
{
  "document_id": "uuid",
  "summary_length": "medium"
}
```

**Response:**
```json
{
  "summary": "The document discusses...",
  "word_count": 150
}
```

---

## 📊 Testing Workflow

```
1. Start API
   python run.py

2. Check health
   Verify API is running

3. Register/Login
   Get authentication token

4. Upload document
   Get document ID

5. Wait for processing
   Usually 2-5 seconds

6. Test operations
   - Search
   - Chat
   - Summarize

7. Cleanup
   Delete test documents
```

---

## 🔐 Authentication

All protected endpoints require a bearer token in the Authorization header:

```bash
# Format
Authorization: Bearer <token>

# Example with cURL
curl -H "Authorization: Bearer eyJ0eXAi..." \
     http://localhost:8000/api/v1/documents
```

**How to get a token:**

```bash
# 1. Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_email@example.com",
    "password": "your_password"
  }'

# 2. Response includes token
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}

# 3. Use token in subsequent requests
TOKEN="eyJ0eXAiOiJKV1QiLCJhbGc..."
curl -H "Authorization: Bearer $TOKEN" \
     http://localhost:8000/api/v1/documents
```

---

## 📁 Files Created

| File | Size | Purpose |
|------|------|---------|
| `test_api.py` | 14.7 KB | Python automated test suite |
| `API_TESTING_WITH_CURL.sh` | 6.2 KB | cURL command examples |
| `API_Testing_PowerShell.ps1` | 16.3 KB | PowerShell test functions |
| `Postman_Collection.json` | 9.4 KB | Postman collection |
| `API_TESTING_GUIDE.md` | 13.3 KB | Complete testing guide |

**Total: 59.9 KB of testing resources**

---

## ✅ Recommended Setup

### For Beginners
1. Start with **Swagger UI** (`http://localhost:8000/docs`)
2. Understand the endpoints visually
3. Move to Python script for automation

### For Development
1. Use **Python script** for validation
2. Use **cURL** for quick manual testing
3. Integrate with CI/CD pipeline

### For Production Testing
1. Use **Postman** for team collaboration
2. Set up test automation with **Python**
3. Monitor with logs and metrics

### For Windows Users
1. Use **PowerShell script** for native integration
2. Use **Swagger UI** for visual testing
3. Use **Postman** for professional testing

---

## 🐛 Troubleshooting

### API not responding
```bash
# Check if running
curl http://localhost:8000/health

# If not running, start it
python run.py
```

### Authentication error
```bash
# Make sure you're logged in
# Get new token with login endpoint
# Include token in Authorization header
```

### Document not found
```bash
# List documents first to get correct ID
curl http://localhost:8000/api/v1/documents \
  -H "Authorization: Bearer $TOKEN"

# Use the document_id from response
```

### Processing takes too long
```bash
# Documents are processed asynchronously
# Wait 3-5 seconds then check status
# Check Celery worker logs

celery -A app.tasks.celery_tasks inspect active
```

---

## 🎓 Learning Path

1. **Understand the API**
   - Read `PROJECT_DOCUMENTATION.md`
   - Review `API_TESTING_GUIDE.md`

2. **See it work**
   - Open Swagger UI at `/docs`
   - Click around, test endpoints

3. **Automate testing**
   - Run `python test_api.py`
   - See all tests execute

4. **Use your preferred tool**
   - Python → CI/CD integration
   - cURL → Scripts and shell automation
   - PowerShell → Windows workflows
   - Postman → Team collaboration

5. **Build your flows**
   - Create test documents
   - Search and chat
   - Monitor responses
   - Debug issues

---

## 🚀 Next Steps

1. **Choose your testing method** from the 5 options
2. **Run the health check** to verify API works
3. **Follow the testing workflow** (register → upload → search)
4. **Integrate into your process** (CI/CD, automation, etc.)
5. **Refer back to guides** as needed

---

## 📞 Quick Reference

| What | Command |
|------|---------|
| **API Docs** | `http://localhost:8000/docs` |
| **Health** | `curl http://localhost:8000/health` |
| **Python Tests** | `python test_api.py` |
| **PowerShell Tests** | `. .\API_Testing_PowerShell.ps1; Run-AllTests` |
| **Manual Testing** | See `API_TESTING_WITH_CURL.sh` |
| **Postman** | Import `Postman_Collection.json` |

---

**Happy Testing! 🎉**

Choose your favorite testing method and start exploring the API!
