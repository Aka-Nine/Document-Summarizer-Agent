#!/usr/bin/env python
"""
API Testing Guide - Comprehensive examples for testing the platform
"""

import requests
import json
from typing import Dict, Any, Optional
import time

# ============================================================================
# CONFIGURATION
# ============================================================================

# Base URL (change if running on different host/port)
API_BASE_URL = "http://localhost:8000"
API_V1_PREFIX = f"{API_BASE_URL}/api/v1"

# Test user credentials
TEST_USER = {
    "username": "testuser@example.com",
    "email": "testuser@example.com",
    "password": "TestPassword123!",
    "full_name": "Test User"
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def print_request(method: str, endpoint: str, headers: Optional[Dict] = None, body: Optional[Dict] = None):
    """Print formatted request information"""
    print(f"\n{'='*70}")
    print(f"📤 {method} {endpoint}")
    if headers:
        print(f"Headers: {json.dumps(headers, indent=2)}")
    if body:
        print(f"Body: {json.dumps(body, indent=2)}")
    print('='*70)

def print_response(response: requests.Response, title: str = "Response"):
    """Print formatted response information"""
    print(f"\n{'='*70}")
    print(f"📥 {title} (Status: {response.status_code})")
    print('='*70)
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

def print_success(message: str):
    """Print success message"""
    print(f"\n✅ {message}")

def print_error(message: str):
    """Print error message"""
    print(f"\n❌ {message}")

# ============================================================================
# TEST SUITE 1: HEALTH & STATUS
# ============================================================================

class HealthTests:
    """Test health check endpoints"""
    
    @staticmethod
    def test_health_check():
        """Test basic health endpoint"""
        print_request("GET", f"{API_BASE_URL}/health")
        response = requests.get(f"{API_BASE_URL}/health")
        print_response(response, "Health Check")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                print_success("API is healthy")
                return True
        print_error("API health check failed")
        return False
    
    @staticmethod
    def test_api_docs():
        """Test API documentation availability"""
        print_request("GET", f"{API_BASE_URL}/docs")
        response = requests.get(f"{API_BASE_URL}/docs")
        
        if response.status_code == 200:
            print_success("API documentation available at /docs")
            return True
        print_error("API documentation not available")
        return False

# ============================================================================
# TEST SUITE 2: AUTHENTICATION
# ============================================================================

class AuthTests:
    """Test authentication endpoints"""
    
    def __init__(self):
        self.auth_token = None
        self.user_id = None
    
    def test_user_registration(self):
        """Test user registration"""
        endpoint = f"{API_V1_PREFIX}/auth/register"
        body = TEST_USER
        
        print_request("POST", endpoint, body=body)
        response = requests.post(endpoint, json=body)
        print_response(response, "Registration Response")
        
        if response.status_code in [200, 201]:
            data = response.json()
            self.user_id = data.get("user_id")
            print_success(f"User registered successfully. User ID: {self.user_id}")
            return True
        elif response.status_code == 409:
            print_error("User already exists (409 Conflict)")
            return True  # User exists, continue with login
        else:
            print_error(f"Registration failed: {response.text}")
            return False
    
    def test_user_login(self):
        """Test user login"""
        endpoint = f"{API_V1_PREFIX}/auth/login"
        body = {
            "username": TEST_USER["username"],
            "password": TEST_USER["password"]
        }
        
        print_request("POST", endpoint, body=body)
        response = requests.post(endpoint, json=body)
        print_response(response, "Login Response")
        
        if response.status_code == 200:
            data = response.json()
            self.auth_token = data.get("access_token") or data.get("token")
            print_success(f"User logged in successfully. Token received.")
            return True
        else:
            print_error(f"Login failed: {response.text}")
            return False
    
    def get_auth_headers(self) -> Dict[str, str]:
        """Get authorization headers"""
        if not self.auth_token:
            print_error("No auth token available. Run test_user_login first.")
            return {}
        return {"Authorization": f"Bearer {self.auth_token}"}

# ============================================================================
# TEST SUITE 3: DOCUMENT OPERATIONS
# ============================================================================

class DocumentTests:
    """Test document upload and management endpoints"""
    
    def __init__(self, auth_headers: Dict[str, str]):
        self.auth_headers = auth_headers
        self.document_id = None
    
    def test_document_upload(self, file_path: str = None):
        """Test document upload"""
        endpoint = f"{API_V1_PREFIX}/documents/upload"
        
        # Create a test file if not provided
        if not file_path:
            file_path = "test_document.txt"
            with open(file_path, 'w') as f:
                f.write("This is a test document for the API. " * 50)
            print(f"Created test file: {file_path}")
        
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {
                'title': 'Test Document',
                'description': 'Test document for API testing'
            }
            
            print_request("POST", endpoint, headers=self.auth_headers)
            response = requests.post(
                endpoint,
                files=files,
                data=data,
                headers=self.auth_headers
            )
        
        print_response(response, "Document Upload Response")
        
        if response.status_code in [200, 201, 202]:
            data = response.json()
            self.document_id = data.get("document_id")
            print_success(f"Document uploaded. ID: {self.document_id}")
            print(f"Status: {data.get('status', 'unknown')}")
            return True
        else:
            print_error(f"Document upload failed: {response.text}")
            return False
    
    def test_get_document(self):
        """Test get document details"""
        if not self.document_id:
            print_error("No document ID. Run test_document_upload first.")
            return False
        
        endpoint = f"{API_V1_PREFIX}/documents/{self.document_id}"
        print_request("GET", endpoint, headers=self.auth_headers)
        response = requests.get(endpoint, headers=self.auth_headers)
        print_response(response, "Get Document Response")
        
        if response.status_code == 200:
            print_success("Document retrieved successfully")
            return True
        else:
            print_error(f"Get document failed: {response.text}")
            return False
    
    def test_list_documents(self):
        """Test list documents"""
        endpoint = f"{API_V1_PREFIX}/documents?page=1&page_size=10"
        print_request("GET", endpoint, headers=self.auth_headers)
        response = requests.get(endpoint, headers=self.auth_headers)
        print_response(response, "List Documents Response")
        
        if response.status_code == 200:
            print_success("Documents listed successfully")
            return True
        else:
            print_error(f"List documents failed: {response.text}")
            return False
    
    def test_delete_document(self):
        """Test delete document"""
        if not self.document_id:
            print_error("No document ID. Run test_document_upload first.")
            return False
        
        endpoint = f"{API_V1_PREFIX}/documents/{self.document_id}"
        print_request("DELETE", endpoint, headers=self.auth_headers)
        response = requests.delete(endpoint, headers=self.auth_headers)
        print_response(response, "Delete Document Response")
        
        if response.status_code == 200:
            print_success("Document deleted successfully")
            return True
        else:
            print_error(f"Delete document failed: {response.text}")
            return False

# ============================================================================
# TEST SUITE 4: SEARCH & RETRIEVAL
# ============================================================================

class SearchTests:
    """Test search and retrieval endpoints"""
    
    def __init__(self, auth_headers: Dict[str, str]):
        self.auth_headers = auth_headers
    
    def test_semantic_search(self, query: str = "test"):
        """Test semantic search"""
        endpoint = f"{API_V1_PREFIX}/search"
        params = {
            "q": query,
            "top_k": 5
        }
        
        print_request("GET", f"{endpoint}?q={query}&top_k=5", headers=self.auth_headers)
        response = requests.get(endpoint, params=params, headers=self.auth_headers)
        print_response(response, "Search Response")
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            print_success(f"Search returned {len(results)} results")
            return True
        else:
            print_error(f"Search failed: {response.text}")
            return False

# ============================================================================
# TEST SUITE 5: CHAT & QA
# ============================================================================

class ChatTests:
    """Test chat and question-answering endpoints"""
    
    def __init__(self, auth_headers: Dict[str, str], document_id: str = None):
        self.auth_headers = auth_headers
        self.document_id = document_id
    
    def test_chat(self, message: str = "What is this document about?"):
        """Test chat endpoint"""
        endpoint = f"{API_V1_PREFIX}/chat"
        body = {
            "message": message,
            "document_id": self.document_id
        }
        
        print_request("POST", endpoint, headers=self.auth_headers, body=body)
        response = requests.post(endpoint, json=body, headers=self.auth_headers)
        print_response(response, "Chat Response")
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Chat response received")
            return True
        else:
            print_error(f"Chat failed: {response.text}")
            return False
    
    def test_summarize(self):
        """Test summarization endpoint"""
        if not self.document_id:
            print_error("No document ID. Run document upload first.")
            return False
        
        endpoint = f"{API_V1_PREFIX}/summarize"
        body = {
            "document_id": self.document_id,
            "summary_length": "medium"
        }
        
        print_request("POST", endpoint, headers=self.auth_headers, body=body)
        response = requests.post(endpoint, json=body, headers=self.auth_headers)
        print_response(response, "Summarize Response")
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Summary generated")
            return True
        else:
            print_error(f"Summarization failed: {response.text}")
            return False

# ============================================================================
# RUN ALL TESTS
# ============================================================================

def run_all_tests():
    """Run complete test suite"""
    print("\n" + "="*70)
    print("ENTERPRISE DOCUMENT INTELLIGENCE PLATFORM - API TEST SUITE".center(70))
    print("="*70)
    print(f"Target: {API_BASE_URL}\n")
    
    # Health checks
    print("\n" + "="*70)
    print("SECTION 1: HEALTH & STATUS CHECKS")
    print("="*70)
    health_tests = HealthTests()
    health_tests.test_health_check()
    time.sleep(1)
    health_tests.test_api_docs()
    
    # Authentication
    print("\n" + "="*70)
    print("SECTION 2: AUTHENTICATION")
    print("="*70)
    auth_tests = AuthTests()
    auth_tests.test_user_registration()
    time.sleep(1)
    auth_tests.test_user_login()
    auth_headers = auth_tests.get_auth_headers()
    
    if not auth_headers:
        print_error("Authentication failed. Cannot continue with other tests.")
        return
    
    # Document operations
    print("\n" + "="*70)
    print("SECTION 3: DOCUMENT OPERATIONS")
    print("="*70)
    doc_tests = DocumentTests(auth_headers)
    doc_tests.test_document_upload()
    time.sleep(2)
    doc_tests.test_get_document()
    time.sleep(1)
    doc_tests.test_list_documents()
    
    # Search & retrieval
    print("\n" + "="*70)
    print("SECTION 4: SEARCH & RETRIEVAL")
    print("="*70)
    search_tests = SearchTests(auth_headers)
    search_tests.test_semantic_search("test")
    
    # Chat & QA
    print("\n" + "="*70)
    print("SECTION 5: CHAT & QUESTION ANSWERING")
    print("="*70)
    chat_tests = ChatTests(auth_headers, doc_tests.document_id)
    chat_tests.test_chat("What is the main topic?")
    time.sleep(1)
    chat_tests.test_summarize()
    
    # Cleanup
    print("\n" + "="*70)
    print("SECTION 6: CLEANUP")
    print("="*70)
    doc_tests.test_delete_document()
    
    print("\n" + "="*70)
    print("TEST SUITE COMPLETED".center(70))
    print("="*70)

if __name__ == "__main__":
    try:
        run_all_tests()
    except Exception as e:
        print_error(f"Test suite error: {str(e)}")
        import traceback
        traceback.print_exc()
