#!/usr/bin/env python3
"""Process final_report.pdf - output to file and display"""
import sys
import os
import asyncio
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

OUTPUT = "report_output.txt"

async def main():
    pdf = Path("docs/final_report.pdf")
    
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\nFINAL REPORT PROCESSING\n" + "=" * 80 + "\n\n")
        f.write(f"File: {pdf}\n")
        
        if not pdf.exists():
            f.write("ERROR: File not found!\n")
            print("ERROR: File not found!")
            return
        
        f.write(f"Size: {pdf.stat().st_size / 1024:.2f} KB\n\n")
        print(f"Processing {pdf}...")
        
        try:
            from app.core.enterprise_document_processor import EnterpriseDocumentProcessor
            
            f.write("Loading...\n")
            f.flush()
            processor = EnterpriseDocumentProcessor()
            processor.document_id = None
            docs = processor.load_document(str(pdf))
            f.write(f"Loaded {len(docs)} pages\n\n")
            f.flush()
            
            f.write("Processing with AI...\n")
            f.flush()
            
            result = await processor.process_document(
                file_path=str(pdf),
                questions=[
                    "What is the main topic of this document?",
                    "What are the key points?",
                    "What are the main conclusions?",
                ],
                metadata={}
            )
            
            f.write("\n" + "=" * 80 + "\nSUMMARY\n" + "=" * 80 + "\n\n")
            f.write(result.get("summary", "No summary") + "\n\n")
            f.flush()
            
            f.write("=" * 80 + "\nQUESTIONS & ANSWERS\n" + "=" * 80 + "\n\n")
            for q, a in result.get("answers", {}).items():
                f.write(f"Q: {q}\n" + "-" * 80 + "\n" + f"A: {a}\n\n")
            f.flush()
            
            f.write("=" * 80 + "\nMETADATA\n" + "=" * 80 + "\n")
            m = result.get("metadata", {})
            f.write(f"Time: {m.get('processing_time', 0):.2f}s\n")
            f.write(f"Pages: {m.get('total_pages', 0)}\n")
            f.write("=" * 80 + "\n")
            
            print(f"Done! Results in {OUTPUT}")
            
            # Display
            f.seek(0)
            print(f.read())
            
        except Exception as e:
            err = f"ERROR: {e}"
            print(err)
            f.write(err + "\n")
            import traceback
            f.write(traceback.format_exc())

if __name__ == "__main__":
    asyncio.run(main())
