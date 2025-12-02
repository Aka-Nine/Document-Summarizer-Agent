#!/bin/bash
# ============================================================================
# API TESTING WITH CURL - Command Line Examples
# ============================================================================
# Run these commands in your terminal to test the API
# Make sure the FastAPI server is running on http://localhost:8000

# BASE CONFIGURATION
API_BASE="http://localhost:8000"
API_V1="$API_BASE/api/v1"
AUTH_TOKEN=""  # Will be set after login

# ============================================================================
# 1. HEALTH CHECK
# ============================================================================

# Test if API is running
echo "Testing API health..."
curl -X GET "$API_BASE/health" -H "Content-Type: application/json"

# View API documentation
echo "Opening API docs..."
echo "Visit: $API_BASE/docs"

# ============================================================================
# 2. USER REGISTRATION
# ============================================================================

# Register a new user
echo "Registering user..."
curl -X POST "$API_V1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser@example.com",
    "password": "TestPassword123!",
    "full_name": "Test User"
  }'

# ============================================================================
# 3. USER LOGIN
# ============================================================================

# Login and get authentication token
echo "Logging in..."
RESPONSE=$(curl -s -X POST "$API_V1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser@example.com",
    "password": "TestPassword123!"
  }')

echo $RESPONSE

# Extract token (requires jq)
# AUTH_TOKEN=$(echo $RESPONSE | jq -r '.access_token')
# echo "Auth token: $AUTH_TOKEN"

# ============================================================================
# 4. DOCUMENT UPLOAD
# ============================================================================

# Create a test file
echo "Creating test document..."
echo "This is a test document for API testing. This content will be processed and indexed." > test_doc.txt

# Upload document (requires valid AUTH_TOKEN)
echo "Uploading document..."
curl -X POST "$API_V1/documents/upload" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -F "file=@test_doc.txt" \
  -F "title=Test Document" \
  -F "description=Test document for API"

# ============================================================================
# 5. GET DOCUMENT DETAILS
# ============================================================================

# Replace DOCUMENT_ID with actual ID from upload response
DOCUMENT_ID="your_document_id_here"

echo "Getting document details..."
curl -X GET "$API_V1/documents/$DOCUMENT_ID" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json"

# ============================================================================
# 6. LIST DOCUMENTS
# ============================================================================

echo "Listing documents..."
curl -X GET "$API_V1/documents?page=1&page_size=10" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json"

# ============================================================================
# 7. SEARCH DOCUMENTS
# ============================================================================

echo "Searching documents..."
curl -X GET "$API_V1/search?q=test&top_k=5" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json"

# ============================================================================
# 8. CHAT / QUESTION ANSWERING
# ============================================================================

echo "Asking question (RAG)..."
curl -X POST "$API_V1/chat" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is this document about?",
    "document_id": "DOCUMENT_ID"
  }'

# ============================================================================
# 9. SUMMARIZE DOCUMENT
# ============================================================================

echo "Generating summary..."
curl -X POST "$API_V1/summarize" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "DOCUMENT_ID",
    "summary_length": "medium"
  }'

# ============================================================================
# 10. DELETE DOCUMENT
# ============================================================================

echo "Deleting document..."
curl -X DELETE "$API_V1/documents/$DOCUMENT_ID" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json"

# ============================================================================
# HELPER: Pretty print JSON
# ============================================================================

# Add ' | jq .' to any curl command to pretty-print JSON output
# Example:
curl -s -X GET "$API_BASE/health" | jq .

# ============================================================================
# HELPER: Save response to file
# ============================================================================

# Use -o flag to save response
curl -X GET "$API_V1/documents" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -o documents_response.json

# ============================================================================
# HELPER: View response headers
# ============================================================================

# Use -i flag to include response headers
curl -i -X GET "$API_BASE/health"

# ============================================================================
# NOTES
# ============================================================================

# 1. Replace YOUR_TOKEN_HERE with actual token from login
# 2. Replace DOCUMENT_ID with actual document ID from upload
# 3. Use -v flag for verbose output (shows request/response details)
# 4. Use -H to add headers
# 5. Use -d for request body (JSON)
# 6. Use -F for multipart/form-data (file uploads)
# 7. Use -X to specify HTTP method (GET, POST, PUT, DELETE, etc.)
