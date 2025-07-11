import requests
import os
from pathlib import Path

BASE_URL = "http://localhost:8000"
USERNAME = "testuser"
PASSWORD = "testpass123"

# 1. Login to get access token
def login():
    data = {"username": USERNAME, "password": PASSWORD}
    response = requests.post(f"{BASE_URL}/login", data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print("Login failed:", response.text)
        return None

def upload_document(token):
    # Create a test PDF file
    test_file_path = "docs/text.pdf"
    # Ensure the file exists or create a dummy PDF for testing
    if not os.path.exists(test_file_path):
        with open(test_file_path, "wb") as f:
            f.write(b"%PDF-1.5\n%Test PDF file for upload testing\n")

    try:
        # Prepare the upload request
        with open(test_file_path, "rb") as file_obj:
            files = {"file": ("text.pdf", file_obj, "application/pdf")}
            data = {
                "questions": "What is this document about?\nWhat are the main goals?"
            }
            headers = {"Authorization": f"Bearer {token}"}
            
            # Make the upload request
            print("\nSending upload request to:", f"{BASE_URL}/upload")
            print("Request files:", files)
            print("Request data:", data)
            response = requests.post(f"{BASE_URL}/upload", files=files, data=data, headers=headers)
            
            print("\nUpload Response:")
            print(f"Status Code: {response.status_code}")
            print(f"Response Body: {response.json()}")
            
            if response.status_code == 200:
                doc_id = response.json()["document_id"]
                print(f"\nDocument uploaded successfully with ID: {doc_id}")
                
                # Check document status
                check_status(doc_id, token)
                
                return doc_id
            else:
                print(f"\nUpload failed: {response.text}")
                
    except Exception as e:
        print(f"Error during testing: {str(e)}")
    finally:
        # Cleanup
        if os.path.exists(test_file_path):
            os.remove(test_file_path)

    return None

def check_status(doc_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/documents/{doc_id}", headers=headers)
    print("\nDocument Status:")
    print("Status Code:", response.status_code)
    print("Status Response:", response.json())

if __name__ == "__main__":
    token = login()
    if token:
        doc_id = upload_document(token)
        if doc_id:
            check_status(doc_id, token) 