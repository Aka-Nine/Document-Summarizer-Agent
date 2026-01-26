#!/usr/bin/env python3
"""Test processing final_report.pdf"""
import sys
import os
import asyncio
from pathlib import Path
import pytest

pytestmark = pytest.mark.skip(reason="Manual integration sample; skipped in automated test runs")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

async def test():
    try:
        pdf = Path("docs/final_report.pdf")
        print(f"File exists: {pdf.exists()}")
        if not pdf.exists():
            return
        
        print("Importing processor...")
        from app.core.enterprise_document_processor import EnterpriseDocumentProcessor
        
        print("Creating processor...")
        processor = EnterpriseDocumentProcessor()
        processor.document_id = None
        
        print("Loading PDF...")
        docs = processor.load_document(str(pdf))
        print(f"Loaded {len(docs)} pages")
        
        print("Processing...")
        result = await processor.process_document(
            file_path=str(pdf),
            questions=["What is this document about?"],
            metadata={}
        )
        
        print("\n" + "="*60)
        print("SUMMARY:")
        print("="*60)
        print(result.get("summary", "No summary"))
        
        print("\n" + "="*60)
        print("ANSWERS:")
        print("="*60)
        for q, a in result.get("answers", {}).items():
            print(f"\nQ: {q}")
            print(f"A: {a}")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
