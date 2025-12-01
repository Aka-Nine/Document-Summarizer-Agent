#!/usr/bin/env python3
"""Process final_report.pdf via API and show results"""
import sys
import os
import requests
import json
from pathlib import Path
import time

API_BASE = "http://localhost:8000/api/v1"

def print_section(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)

def main():
    pdf_path = Path("docs/final_report.pdf")
    
    if not pdf_path.exists():
        print(f"ERROR: {pdf_path} not found!")
        return
    
    print_section("PROCESSING FINAL REPORT VIA API")
    print(f"File: {pdf_path}")
    print(f"Size: {pdf_path.stat().st_size / 1024:.2f} KB")
    
    # Check if API is running
    try:
        response = requests.get("http://localhost:8000/test", timeout=5)
        if response.status_code != 200:
            print("ERROR: API server is not responding correctly")
            return
    except:
        print("ERROR: API server is not running. Please start it with: python run.py")
        return
    
    print("\n\u2713 API server is running")
    
    # Register user (if needed) or login
    print("\n1. Registering/Logging in...")
    try:
        # Try to register
        register_data = {
            "username": "test_user",
            "email": "test@example.com",
            "password": "testpass123"
        }
        response = requests.post(f"{API_BASE}/register", json=register_data, timeout=10)
        
        if response.status_code == 200:
            print("\u2713 User registered")
            token = response.json().get("access_token")
        else:
            # Try login
            login_data = {
                "username": "test_user",
                "password": "testpass123"
            }
            response = requests.post(f"{API_BASE}/login", data=login_data, timeout=10)
            if response.status_code == 200:
                print("\u2713 User logged in")
                token = response.json().get("access_token")
            else:
                print(f"ERROR: Could not register or login: {response.text}")
                return
    except Exception as e:
        print(f"ERROR: {e}")
        return
    
    # Upload document
    print("\n2. Uploading document...")
    try:
        with open(pdf_path, "rb") as f:
            files = {"file": (pdf_path.name, f, "application/pdf")}
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(
                f"{API_BASE}/documents/upload",
                files=files,
                headers=headers,
                timeout=60
            )
            
            if response.status_code != 200:
                print(f"ERROR: Upload failed: {response.text}")
                return
            
            doc_data = response.json()
            document_id = doc_data.get("id")
            print(f"\u2713 Document uploaded. ID: {document_id}")
            print(f"  Status: {doc_data.get('status')}")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Wait for processing
    print("\n3. Waiting for processing to complete...")
    print("   (This may take 1-2 minutes)")
    max_wait = 180  # 3 minutes
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        try:
            response = requests.get(
                f"{API_BASE}/documents/{document_id}",
                headers={"Authorization": f"Bearer {token}"},
                timeout=10
            )
            
            if response.status_code == 200:
                doc = response.json()
                status = doc.get("status")
                print(f"   Status: {status}")
                
                if status == "completed":
                    print("\n\u2713 Processing complete!")
                    break
                elif status == "failed":
                    print(f"\n\u2717 Processing failed: {doc.get('error_message', 'Unknown error')}")
                    return
        except:
            pass
        
        time.sleep(5)
    
    # Get results
    print("\n4. Retrieving results...")
    try:
        response = requests.get(
            f"{API_BASE}/documents/{document_id}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        
        if response.status_code == 200:
            doc = response.json()
            
            print_section("SUMMARY")
            print(doc.get("summary", "No summary available"))
            
            print_section("QUESTIONS & ANSWERS")
            qa_results = doc.get("qa_results", {})
            for i, (question, answer) in enumerate(qa_results.items(), 1):
                print(f"\nQ{i}: {question}")
                print("-" * 80)
                print(answer)
            
            print_section("METADATA")
            print(f"Processing Time: {doc.get('processing_time', 0):.2f} seconds")
            print(f"Total Pages: {len(doc.get('summary', '').split())} (estimated)")
            print(f"RAG Enabled: {doc.get('rag_enabled', False)}")
            
            print_section("\u2705 COMPLETE")
        else:
            print(f"ERROR: Could not retrieve results: {response.text}")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
