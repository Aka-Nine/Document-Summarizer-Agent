#!/usr/bin/env python3
"""Process final_report.pdf and show output"""
import sys
import os
import asyncio
from pathlib import Path
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

OUTPUT_FILE = "final_report_output.txt"

async def process():
    pdf_path = Path("docs/final_report.pdf")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("=" * 80 + "\n")
        out.write("FINAL REPORT PROCESSING RESULTS\n")
        out.write("=" * 80 + "\n\n")
        
        if not pdf_path.exists():
            msg = f"ERROR: {pdf_path} not found!"
            out.write(msg + "\n")
            print(msg)
            return
        
        out.write(f"File: {pdf_path}\n")
        out.write(f"Size: {pdf_path.stat().st_size / 1024:.2f} KB\n\n")
        print(f"Processing {pdf_path}...")
        
        try:
            from app.core.enterprise_document_processor import EnterpriseDocumentProcessor
            from app.config.settings import settings
            
            out.write(f"LLM Provider: {settings.LLM_PROVIDER}\n")
            out.write(f"RAG Enabled: {settings.RAG_ENABLED}\n\n")
            out.flush()
            
            print("Loading document...")
            processor = EnterpriseDocumentProcessor()
            processor.document_id = None
            documents = processor.load_document(str(pdf_path))
            out.write(f"Loaded {len(documents)} pages\n\n")
            out.flush()
            print(f"Loaded {len(documents)} pages")
            
            questions = [
                "What is the main topic or theme of this document?",
                "What are the key points or arguments presented?",
                "What are the main conclusions or recommendations?",
                "What important facts, figures, or statistics are mentioned?",
            ]
            
            print("Processing with AI (this may take 1-2 minutes)...")
            out.write("Processing with AI...\n")
            out.flush()
            
            result = await processor.process_document(
                file_path=str(pdf_path),
                questions=questions,
                metadata={"filename": "final_report.pdf"}
            )
            
            # Write results
            out.write("\n" + "=" * 80 + "\n")
            out.write("SUMMARY\n")
            out.write("=" * 80 + "\n\n")
            summary = result.get("summary", "No summary generated")
            out.write(summary + "\n\n")
            out.flush()
            
            out.write("=" * 80 + "\n")
            out.write("QUESTIONS & ANSWERS\n")
            out.write("=" * 80 + "\n\n")
            for q, a in result.get("answers", {}).items():
                out.write(f"Q: {q}\n")
                out.write("-" * 80 + "\n")
                out.write(f"A: {a}\n\n")
            out.flush()
            
            out.write("=" * 80 + "\n")
            out.write("METADATA\n")
            out.write("=" * 80 + "\n")
            meta = result.get("metadata", {})
            out.write(f"Processing Time: {meta.get('processing_time', 0):.2f} seconds\n")
            out.write(f"Total Pages: {meta.get('total_pages', 0)}\n")
            out.write(f"Total Chunks: {meta.get('total_chunks', 0)}\n")
            out.write(f"RAG Enabled: {meta.get('rag_enabled', False)}\n")
            out.write("=" * 80 + "\n")
            
            print(f"\n\u2705 Processing complete! Results saved to: {OUTPUT_FILE}")
            print(f"\nDisplaying results:\n")
            
            # Display results
            out.seek(0)
            content = out.read()
            print(content)
            
    except Exception as e:
        error = f"ERROR: {e}"
        print(error)
        import traceback
        traceback.print_exc()
        if 'out' in locals():
            out.write(error + "\n")
            out.write(traceback.format_exc())
