import requests
import os
import json
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def register(username, password, email):
    url = "http://localhost:8000/register"
    data = {"username": username, "password": password, "email": email}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print(f"✅ Registered: {username}")
        return True
    else:
        print(f"❌ Registration failed: {response.text}")
        return False

def login(username, password):
    url = "http://localhost:8000/login"
    data = {"username": username, "password": password}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("❌ Login failed:", response.text)
        return None

def test_upload():
    os.makedirs('docs', exist_ok=True)
    test_file_path = 'docs/sample.pdf'


    username = f"testuser_{int(time.time())}"
    password = "testpassword"
    email = f"{username}@example.com"

    # Register user
    if not register(username, password, email):
        return

    # Login user
    token = login(username, password)
    if not token:
        print("❌ Could not obtain token")
        return

    # Prepare upload
    headers = {"Authorization": f"Bearer {token}"}
    files = {'file': ('sample.pdf', open(test_file_path, 'rb'), 'application/pdf')}
    data = {
        'questions': 'What is this document about?, What are the key points?, What is the conclusion?'
    }

    print("📤 Uploading file...")
    response = requests.post('http://localhost:8000/upload', files=files, data=data, headers=headers)
    print("Upload response:", response.status_code, response.text)

    if response.status_code != 200:
        return

    document_id = response.json().get("document_id")
    if not document_id:
        print("❌ Document ID not found")
        return

    # Wait and poll for result
    print("⏳ Waiting for processing to complete...")
    for attempt in range(10):
        time.sleep(3)
        result_response = requests.get(f"http://localhost:8000/documents/{document_id}", headers=headers)
        result_data = result_response.json()
        if result_data.get("status") in ["completed", "failed"]:
            break

    print("\n=== Document Processing Results ===")
    print(f"📄 Status: {result_data.get('status')}")
    print(f"⏱ Processing Time: {result_data.get('processing_time', 0)}s")

    print("\n📝 Summary:\n", result_data.get("summary", "No summary available"))

    print("\n❓ Q&A Results:")
    qa_results = result_data.get("qa_results")

    if isinstance(qa_results, dict):
        for question, answer in qa_results.items():
            print(f"\nQ: {question}\nA: {answer}")
    else:
        print("No Q&A available or unexpected format.")

if __name__ == "__main__":
    test_upload()
