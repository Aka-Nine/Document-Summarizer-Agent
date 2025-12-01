# API Testing Guide - Enterprise Document Intelligence Platform

## 📋 Quick Start

You have **4 ways** to test the API:

1. **Swagger UI** - Interactive web interface (easiest)
2. **Python Script** - Automated test suite
3. **cURL** - Command-line testing
4. **Postman** - Desktop application testing

---

## Method 1: Swagger UI (Easiest) 🌐

### What is Swagger UI?
Swagger UI is an interactive API documentation interface built into FastAPI. You can test endpoints directly in your browser.

### How to Access

1. **Start the API server:**
   ```bash
   python run.py
   ```
   Server runs on `http://localhost:8000`

2. **Open Swagger UI:**
   - Go to: `http://localhost:8000/docs`
   - You'll see a beautiful interface with all endpoints

3. **Test an Endpoint:**
   - Click on any endpoint (e.g., GET /health)
   - Click "Try it out" button
   - Fill in any parameters
   - Click "Execute"
   - See the response!

### Example: Testing Health Check
```
1. Go to http://localhost:8000/docs
2. Find "GET /health"
3. Click "Try it out"
4. Click "Execute"
5. See response: {"status": "healthy", "database": "connected", ...}
```

### Advantages
✅ No installation needed
✅ Visual interface
✅ See request/response in real-time
✅ Built-in documentation
✅ Can test file uploads directly

---

## Method 2: Python Script Testing 🐍

### Setup

```bash
# Install required library (if not already installed)
pip install requests

# Run the test script
python test_api.py
```

### What the Script Does

The `test_api.py` script includes:

```python
1. Health Checks
   - Test API is running
   - Test docs are available

2. Authentication
   - Register new user
   - User login
   - Get auth token

3. Document Operations
   - Upload document
   - Get document details
   - List documents
   - Delete document

4. Search & Retrieval
   - Perform semantic search

5. Chat & QA
   - Chat with document
   - Generate summary
```

### Running Individual Tests

```bash
# Run all tests
python test_api.py

# Run specific test (requires modifying script)
python -c "
from test_api import HealthTests
health = HealthTests()
health.test_health_check()
"
```

### Expected Output

```
======================================================================
                    API TEST SUITE
======================================================================
Target: http://localhost:8000

======================================================================
SECTION 1: HEALTH & STATUS CHECKS
======================================================================

======================================================================
📤 GET http://localhost:8000/health
======================================================================

======================================================================
📥 Health Check (Status: 200)
======================================================================
{
  "status": "healthy",
  "database": "connected",
  "redis": "connected",
  "vector_db": "connected"
}

✅ API is healthy
...
```

### Using the Test Classes

```python
from test_api import AuthTests, DocumentTests, SearchTests

# 1. Authenticate
auth = AuthTests()
auth.test_user_registration()
auth.test_user_login()
headers = auth.get_auth_headers()

# 2. Upload document
docs = DocumentTests(headers)
docs.test_document_upload("my_document.pdf")

# 3. Search
search = SearchTests(headers)
search.test_semantic_search("search query")
```

---

## Method 3: cURL (Command Line) 💻

### Prerequisites

- cURL installed (usually built-in on Mac/Linux)
- For Windows: Download from https://curl.se/download.html

### Basic Commands

```bash
# Test health
curl http://localhost:8000/health

# Register user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user@example.com",
    "password": "Password123!",
    "full_name": "User Name"
  }'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user@example.com",
    "password": "Password123!"
  }'

# Save auth token (with jq installed)
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user@example.com","password":"Password123!"}' | jq -r '.access_token')

# Upload document (with token)
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@document.pdf" \
  -F "title=My Document"

# List documents
curl -X GET http://localhost:8000/api/v1/documents \
  -H "Authorization: Bearer $TOKEN"

# Search
curl -X GET "http://localhost:8000/api/v1/search?q=test&top_k=5" \
  -H "Authorization: Bearer $TOKEN"
```

### Pretty Print JSON

Add `| jq` to any command to format JSON nicely:

```bash
curl -s http://localhost:8000/health | jq
```

### cURL Flags Reference

| Flag | Purpose | Example |
|------|---------|---------|
| `-X` | HTTP method | `-X POST` |
| `-H` | Header | `-H "Content-Type: application/json"` |
| `-d` | Request body (JSON) | `-d '{"key":"value"}'` |
| `-F` | Form data (files) | `-F "file=@file.pdf"` |
| `-i` | Include headers | `curl -i http://...` |
| `-v` | Verbose (show details) | `curl -v http://...` |
| `-o` | Save to file | `-o response.json` |
| `-s` | Silent mode | `curl -s http://...` |

### Complete cURL Workflow

See `API_TESTING_WITH_CURL.sh` in the project root for complete examples.

---

## Method 4: Postman (Desktop App) 📮

### Setup

1. **Download Postman:**
   - Go to https://www.postman.com/downloads/
   - Install for your OS

2. **Import Collection:**
   - Open Postman
   - Click "Import"
   - Select `Postman_Collection.json` from the project
   - Collection loads with all endpoints ready

3. **Set Variables:**
   - Go to "Environment" settings
   - Set `base_url` = `http://localhost:8000`
   - Variables `auth_token` and `document_id` are auto-set after requests

### Using Postman

1. **Health Check:**
   - Click "Health & Status" → "Health Check"
   - Click "Send"
   - See response

2. **Login:**
   - Click "Authentication" → "User Login"
   - Click "Send"
   - Auth token automatically saved to `{{auth_token}}` variable

3. **Upload Document:**
   - Click "Documents" → "Upload Document"
   - Click "Select Files" to choose a file
   - Click "Send"
   - Document ID automatically saved to `{{document_id}}` variable

4. **Use Saved Variables:**
   - All subsequent requests use `{{auth_token}}` and `{{document_id}}`
   - No manual copying needed!

### Advantages
✅ Beautiful UI
✅ Collection management
✅ Environment variables
✅ Request history
✅ Can create workflows
✅ Export/import collections

---

## API Endpoints Summary

### Health
- `GET /health` - Check API status

### Authentication
- `POST /api/v1/auth/register` - Register user
- `POST /api/v1/auth/login` - Login and get token

### Documents
- `POST /api/v1/documents/upload` - Upload document
- `GET /api/v1/documents` - List documents
- `GET /api/v1/documents/{id}` - Get document details
- `DELETE /api/v1/documents/{id}` - Delete document

### Search
- `GET /api/v1/search?q=query&top_k=5` - Semantic search

### Chat & QA
- `POST /api/v1/chat` - Chat with document (RAG)
- `POST /api/v1/summarize` - Generate summary

---

## Testing Workflow (Recommended)

### Step 1: Verify API is Running

```bash
curl http://localhost:8000/health
# Should return: {"status": "healthy", ...}
```

### Step 2: Register or Login

**Option A: Register (first time)**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser@example.com",
    "password": "TestPassword123!",
    "full_name": "Test User"
  }'
```

**Option B: Login (existing user)**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser@example.com",
    "password": "TestPassword123!"
  }' | jq
```

Copy the `access_token` from response.

### Step 3: Create Test File

```bash
echo "This is a test document with some content about AI and machine learning." > test.txt
```

### Step 4: Upload Document

```bash
TOKEN="your_token_here"
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@test.txt" \
  -F "title=Test Document" | jq
```

Copy the `document_id` from response.

### Step 5: Wait for Processing

Documents are processed asynchronously. Wait a few seconds.

### Step 6: Search Documents

```bash
TOKEN="your_token_here"
curl -X GET "http://localhost:8000/api/v1/search?q=AI&top_k=5" \
  -H "Authorization: Bearer $TOKEN" | jq
```

### Step 7: Chat with Document

```bash
TOKEN="your_token_here"
DOC_ID="your_document_id"
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": \"What is this document about?\",
    \"document_id\": \"$DOC_ID\"
  }" | jq
```

### Step 8: Generate Summary

```bash
TOKEN="your_token_here"
DOC_ID="your_document_id"
curl -X POST http://localhost:8000/api/v1/summarize \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"document_id\": \"$DOC_ID\",
    \"summary_length\": \"medium\"
  }" | jq
```

---

## Common Issues & Solutions

### Issue 1: Connection Refused
```
Error: Failed to connect to localhost:8000
```
**Solution:**
```bash
# Make sure API is running
python run.py

# Check if running on different port
curl http://localhost:8000/health  # or try different port
```

### Issue 2: Unauthorized (401)
```json
{"detail": "Unauthorized"}
```
**Solution:**
```bash
# Make sure token is correct
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user@example.com","password":"password"}' | jq -r '.access_token')

# Use token in Authorization header
curl -H "Authorization: Bearer $TOKEN" ...
```

### Issue 3: File Not Found
```json
{"detail": "Document not found"}
```
**Solution:**
```bash
# Make sure document_id is correct
# List documents first
curl http://localhost:8000/api/v1/documents -H "Authorization: Bearer $TOKEN" | jq

# Copy correct ID and use it
```

### Issue 4: Rate Limited (429)
```json
{"detail": "Rate limit exceeded"}
```
**Solution:**
- Wait before making more requests
- Or reduce rate limit in settings

### Issue 5: Document Still Processing
```json
{"status": "processing"}
```
**Solution:**
- Wait a few seconds for processing to complete
- Check again with GET request

---

## Performance Testing

### Load Testing with Apache Bench

```bash
# Test 1000 requests with 10 concurrent
ab -n 1000 -c 10 http://localhost:8000/health

# View results
# - Requests per second
# - Average response time
# - Min/max times
```

### Load Testing with wrk

```bash
# Test with 4 threads, 100 connections for 30 seconds
wrk -t4 -c100 -d30s http://localhost:8000/health
```

### Load Testing with Locust

```bash
# Install locust
pip install locust

# Create locustfile.py with your test scenarios
# Run locust
locust -f locustfile.py
```

---

## Debugging Tips

### Enable Verbose Output

**cURL:**
```bash
curl -v http://localhost:8000/health
# Shows request/response headers
```

**Python:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
# Will show all requests/responses
```

### Check Server Logs

**Terminal running FastAPI:**
- Watch for errors and warnings
- Check processing status

### Check Celery Tasks

If you have Celery worker running:
```bash
# View task status
celery -A app.tasks.celery_tasks inspect active

# View task results
celery -A app.tasks.celery_tasks inspect active_by_hostname
```

### Check Redis Cache

```bash
# If Redis running locally
redis-cli KEYS "*"
redis-cli GET "key_name"
```

---

## Next Steps

1. **Try all 4 testing methods** to find what works best for you
2. **Run the automated test suite** to verify all endpoints
3. **Create test data** and experiment with search/chat
4. **Check the logs** to understand what's happening
5. **Read PROJECT_DOCUMENTATION.md** for detailed API info

---

## Quick Reference

| Task | Command |
|------|---------|
| Check API health | `curl http://localhost:8000/health` |
| Open docs | Go to `http://localhost:8000/docs` |
| Register user | `curl -X POST .../auth/register -d '{...}'` |
| Login | `curl -X POST .../auth/login -d '{...}'` |
| Upload doc | `curl -X POST .../documents/upload -F "file=@file.pdf"` |
| Search | `curl .../search?q=query -H "Authorization: Bearer $TOKEN"` |
| Chat | `curl -X POST .../chat -d '{"message":"...","document_id":"..."}'` |

---

**Happy Testing! 🚀**
