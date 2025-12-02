#!/usr/bin/env python3
"""Simple script to process final_report.pdf"""
import sys
import os
import asyncio
from pathlib import Path

# Setup
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

async def process():
    pdf_path = Path("docs/final_report.pdf")
    print("=" * 80)
    print("PROCESSING FINAL REPORT")
    print("=" * 80)
    print(f"\nFile: {pdf_path}")
    
    if not pdf_path.exists():
        print(f"ERROR: File not found!")
        return
    
    print(f"Size: {pdf_path.stat().st_size / 1024:.2f} KB\n")
    
    try:
        from app.core.enterprise_document_processor import EnterpriseDocumentProcessor
        
        print("Loading document...")
        processor = EnterpriseDocumentProcessor()
        processor.document_id = None
        documents = processor.load_document(str(pdf_path))
        print(f"Loaded {len(documents)} pages\n")
        
        print("Processing with AI...")
        result = await processor.process_document(
            file_path=str(pdf_path),
            questions=[
                "What is the main topic of this document?",
                "What are the key points?",
                "What are the main conclusions?",
            ],
            metadata={"filename": "final_report.pdf"}
        )
        
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(result.get("summary", "No summary"))
        
        print("\n" + "=" * 80)
        print("QUESTIONS & ANSWERS")
        print("=" * 80)
        for q, a in result.get("answers", {}).items():
            print(f"\nQ: {q}")
            print(f"A: {a}")
        
        print("\n" + "=" * 80)
        print("METADATA")
        print("=" * 80)
        meta = result.get("metadata", {})
        print(f"Time: {meta.get('processing_time', 0):.2f}s")
        print(f"Pages: {meta.get('total_pages', 0)}")
        print("=" * 80)
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(process())
