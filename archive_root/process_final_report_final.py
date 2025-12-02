#!/usr/bin/env python3
"""Direct processing of final_report.pdf with visible output"""
import sys
import os
import asyncio
from pathlib import Path

# Force output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

print("=" * 80, flush=True)
print("PROCESSING FINAL REPORT PDF", flush=True)
print("=" * 80, flush=True)
print()

pdf_path = Path("docs/final_report.pdf")
if not pdf_path.exists():
    print(f"ERROR: {pdf_path} not found!", flush=True)
    sys.exit(1)

print(f"File: {pdf_path}", flush=True)
print(f"Size: {pdf_path.stat().st_size / 1024:.2f} KB", flush=True)
print()

async def process():
    try:
        print("Importing modules...", flush=True)
        from app.core.enterprise_document_processor import EnterpriseDocumentProcessor
        from app.config.settings import settings
        
        print(f"LLM Provider: {settings.LLM_PROVIDER}", flush=True)
        print(f"RAG Enabled: {settings.RAG_ENABLED}", flush=True)
        print()
        
        print("Creating processor...", flush=True)
        processor = EnterpriseDocumentProcessor()
        processor.document_id = None
        
        print("Loading PDF document...", flush=True)
        documents = processor.load_document(str(pdf_path))
        print(f"\u2713 Loaded {len(documents)} pages", flush=True)
        print()
        
        questions = [
            "What is the main topic or theme of this document?",
            "What are the key points or arguments presented?",
            "What are the main conclusions or recommendations?",
        ]
        
        print("\ud83e\udd16 Processing with AI (this may take 1-2 minutes)...", flush=True)
        print("   Please wait...", flush=True)
        print()
        
        result = await processor.process_document(
            file_path=str(pdf_path),
            questions=questions,
            metadata={"filename": "final_report.pdf"}
        )
        
        print()
        print("=" * 80, flush=True)
        print("SUMMARY", flush=True)
        print("=" * 80, flush=True)
        print()
        summary = result.get("summary", "No summary generated")
        print(summary, flush=True)
        print()
        
        print("=" * 80, flush=True)
        print("QUESTIONS & ANSWERS", flush=True)
        print("=" * 80, flush=True)
        print()
        answers = result.get("answers", {})
        for i, (question, answer) in enumerate(answers.items(), 1):
            print(f"Q{i}: {question}", flush=True)
            print("-" * 80, flush=True)
            print(answer, flush=True)
            print()
        
        print("=" * 80, flush=True)
        print("METADATA", flush=True)
        print("=" * 80, flush=True)
        meta = result.get("metadata", {})
        print(f"Processing Time: {meta.get('processing_time', 0):.2f} seconds", flush=True)
        print(f"Total Pages: {meta.get('total_pages', 0)}", flush=True)
        print(f"Total Chunks: {meta.get('total_chunks', 0)}", flush=True)
        print(f"RAG Enabled: {meta.get('rag_enabled', False)}", flush=True)
        print()
        print("=" * 80, flush=True)
        print("\u2705 PROCESSING COMPLETE", flush=True)
        print("=" * 80, flush=True)
        
    except Exception as e:
        print(f"\n\u274c ERROR: {e}", flush=True)
        import traceback
        print(traceback.format_exc(), flush=True)
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(process())
    except KeyboardInterrupt:
        print("\n\n\u26a0 Interrupted by user", flush=True)
        sys.exit(1)
    except Exception as e:
        print(f"\n\u274c Fatal error: {e}", flush=True)
        import traceback
        print(traceback.format_exc(), flush=True)
        sys.exit(1)
