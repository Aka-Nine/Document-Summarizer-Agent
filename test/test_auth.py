import requests
import json

BASE_URL = "http://localhost:8000"

def register_user():
    """Register a new user"""
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/register", data=data)
    print(f"Register: {response.status_code}")
    print(f"Response: {response.text}")
    
    return response.status_code == 200

def login():
    """Login and get access token"""
    data = {
        "username": "testuser",
        "password": "testpass123"
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

def check_document_status(document_id, token):
    """Check document status using the access token"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/documents/{document_id}", headers=headers)
    print(f"Status check: {response.status_code}")
    print(f"Response: {response.text}")
    
    return response.status_code == 200

if __name__ == "__main__":
    # First try to register
    if register_user():
        print("User registered successfully")
    else:
        print("User registration failed or user already exists")
    
    # Then login
    token = login()
    if token:
        # Check document status
        check_document_status(6, token) 