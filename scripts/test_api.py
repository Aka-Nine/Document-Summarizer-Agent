#!/usr/bin/env python3
"""
Simple API testing script
"""
import requests
import json
import time
from pathlib import Path

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_registration():
    """Test user registration"""
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/register", data=data)
    print(f"Registration: {response.status_code}")
    if response.status_code != 200:
        print(f"Error: {response.text}")
    return response.status_code == 200

def test_login():
    """Test user login"""
    data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/login", data=data)
    print(f"Login: {response.status_code}")
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"Access token received")
        return token
    else:
        print(f"Login failed: {response.text}")
        return None

def test_upload(token):
    """Test document upload"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a test file
    test_content = """
    This is a test document for processing.
    
    The main topic is testing the document processing pipeline.
    
    Key points:
    1. Test file upload functionality
    2. Verify document processing works
    3. Check summarization and Q&A features
    
    This document contains important information about system testing.
    The goal is to ensure all components work together properly.
    """
    
    files = {"file": ("test_document.txt", test_content, "text/plain")}
    data = {"questions": "What is this document about?\nWhat are the main goals?"}
    
    response = requests.post(f"{BASE_URL}/upload", 
                           headers=headers, 
                           files=files, 
                           data=data)
    
    print(f"Upload: {response.status_code}")
    if response.status_code == 200:
        doc_id = response.json()["document_id"]
        print(f"Document uploaded with ID: {doc_id}")
        return doc_id
    else:
        print(f"Upload failed: {response.text}")
        return None

def test_document_status(token, doc_id):
    """Check document processing status"""
    headers = {"Authorization": f"Bearer {token}"}
    
    for i in range(10):  # Check for up to 50 seconds
        response = requests.get(f"{BASE_URL}/documents/{doc_id}", headers=headers)
        
        if response.status_code == 200:
            doc_data = response.json()
            status = doc_data["status"]
            print(f"Document status: {status}")
            
            if status == "completed":
                print("Summary:", doc_data["summary"][:100] + "...")
                print("Q&A Results:", list(doc_data["qa_results"].keys())[:2])
                return True
            elif status == "failed":
                print(f"Processing failed: {doc_data['error_message']}")
                return False
        
        time.sleep(5)
    
    print("Processing timeout")
    return False

def main():
    """Run all tests"""
    print("Starting API tests...")
    
    # Test health
    if not test_health():
        print("Health check failed!")
        return
    
    # Test registration
    test_registration()  # May fail if user exists
    
    # Test login
    token = test_login()
    if not token:
        print("Login failed!")
        return
    
    # Test file upload
    doc_id = test_upload(token)
    if not doc_id:
        print("Upload failed!")
        return
    
    # Test document processing
    if test_document_status(token, doc_id):
        print("All tests passed!")
    else:
        print("Document processing test failed!")

if __name__ == "__main__":
    main() 