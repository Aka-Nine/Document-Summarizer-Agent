#!/usr/bin/env python3
"""Process final_report.pdf and save output"""
import sys
import os
import asyncio
from pathlib import Path
from datetime import datetime

# Ensure app package is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

output_file = "final_report_results.txt"

async def main():
    pdf_path = Path("docs/final_report.pdf")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write("FINAL REPORT PROCESSING RESULTS\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"File: {pdf_path}\n")
        
        if not pdf_path.exists():
            f.write("ERROR: File not found!\n")
            print("ERROR: File not found!")
            return
        
        f.write(f"Size: {pdf_path.stat().st_size / 1024:.2f} KB\n\n")
        print(f"Processing {pdf_path}...")
        
        try:
            from app.core.enterprise_document_processor import EnterpriseDocumentProcessor
            from app.config.settings import settings
            
            f.write(f"LLM Provider: {settings.LLM_PROVIDER}\n")
            f.write(f"RAG Enabled: {settings.RAG_ENABLED}\n\n")
            
            f.write("Loading document...\n")
            f.flush()
            processor = EnterpriseDocumentProcessor()
            processor.document_id = None
            documents = processor.load_document(str(pdf_path))
            f.write(f"Loaded {len(documents)} pages\n\n")
            
            f.write("Processing with AI...\n")
            f.flush()
            
            result = await processor.process_document(
                file_path=str(pdf_path),
                questions=[
                    "What is the main topic or theme of this document?",
                    "What are the key points or arguments presented?",
                    "What are the main conclusions or recommendations?",
                    "What important facts, figures, or statistics are mentioned?",
                ],
                metadata={"filename": "final_report.pdf"}
            )
            
            f.write("\n" + "=" * 80 + "\n")
            f.write("SUMMARY\n")
            f.write("=" * 80 + "\n\n")
            f.write(result.get("summary", "No summary generated") + "\n\n")
            
            f.write("=" * 80 + "\n")
            f.write("QUESTIONS & ANSWERS\n")
            f.write("=" * 80 + "\n\n")
            for q, a in result.get("answers", {}).items():
                f.write(f"Q: {q}\n")
                f.write("-" * 80 + "\n")
                f.write(f"A: {a}\n\n")
            
            f.write("=" * 80 + "\n")
            f.write("METADATA\n")
            f.write("=" * 80 + "\n")
            meta = result.get("metadata", {})
            f.write(f"Processing Time: {meta.get('processing_time', 0):.2f} seconds\n")
            f.write(f"Total Pages: {meta.get('total_pages', 0)}\n")
            f.write(f"Total Chunks: {meta.get('total_chunks', 0)}\n")
            f.write(f"RAG Enabled: {meta.get('rag_enabled', False)}\n")
            f.write("=" * 80 + "\n")
            f.write("PROCESSING COMPLETE\n")
            f.write("=" * 80 + "\n")
            
            print(f"Processing complete! Results saved to: {output_file}")
            
        except Exception as e:
            error_msg = f"ERROR: {e}\n"
            f.write(error_msg)
            import traceback
            f.write(traceback.format_exc())
            print(error_msg)
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
