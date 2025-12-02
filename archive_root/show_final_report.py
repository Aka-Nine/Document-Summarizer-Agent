#!/usr/bin/env python3
"""Process and display final_report.pdf output"""
import sys
import os
import asyncio
from pathlib import Path
from datetime import datetime

# Ensure output is flushed
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Also write to file for reliability
output_file = Path("logs") / f"final_report_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
output_file.parent.mkdir(exist_ok=True)

# Load environment
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def print_section(title, file=None):
    """Print a section header"""
    msg = "\n" + "=" * 80 + "\n" + title + "\n" + "=" * 80
    print(msg, flush=True)
    if file:
        file.write(msg + "\n")
        file.flush()

async def main():
    """Main processing function"""
    with open(output_file, "w", encoding="utf-8") as f:
        print_section("PROCESSING FINAL REPORT PDF", f)
        
        pdf_path = Path("docs/final_report.pdf")
        if not pdf_path.exists():
            error_msg = f"\u274c Error: {pdf_path} not found!"
            print(error_msg, flush=True)
            f.write(error_msg + "\n")
            sys.exit(1)
        
        file_info = f"\ud83d\udcc4 File: {pdf_path}\n\ud83d\udcca Size: {pdf_path.stat().st_size / 1024:.2f} KB"
        print(file_info, flush=True)
        f.write(file_info + "\n")
        
        try:
            from app.core.enterprise_document_processor import EnterpriseDocumentProcessor
            from app.config.settings import settings
            
            config_info = f"\n\ud83d\udd27 LLM Provider: {settings.LLM_PROVIDER}\n\ud83d\udd27 RAG Enabled: {settings.RAG_ENABLED}"
            print(config_info, flush=True)
            f.write(config_info + "\n")
            
            print("\n\ud83d\udcd6 Loading document...", flush=True)
            f.write("\n\ud83d\udcd6 Loading document...\n")
            f.flush()
            
            processor = EnterpriseDocumentProcessor()
            documents = processor.load_document(str(pdf_path))
            loaded_msg = f"   \u2713 Loaded {len(documents)} pages"
            print(loaded_msg, flush=True)
            f.write(loaded_msg + "\n")
            
            questions = [
                "What is the main topic or theme of this document?",
                "What are the key points or arguments presented?",
                "What are the main conclusions or recommendations?",
                "What important facts, figures, or statistics are mentioned?",
            ]
            
            print("\n\ud83e\udd16 Processing with AI (this may take a moment)...", flush=True)
            f.write("\n\ud83e\udd16 Processing with AI (this may take a moment)...\n")
            f.flush()
            
            processor.document_id = None  # Skip RAG indexing
            
            result = await processor.process_document(
                file_path=str(pdf_path),
                questions=questions,
                metadata={"filename": "final_report.pdf"}
            )
            
            print_section("SUMMARY", f)
            summary = result.get("summary", "")
            if summary:
                print(summary, flush=True)
                f.write(summary + "\n")
            else:
                msg = "No summary generated"
                print(msg, flush=True)
                f.write(msg + "\n")
            
            print_section("QUESTIONS & ANSWERS", f)
            answers = result.get("answers", {})
            for i, (question, answer) in enumerate(answers.items(), 1):
                qa_text = f"\nQ{i}: {question}\n" + "-" * 80 + "\n" + answer
                print(qa_text, flush=True)
                f.write(qa_text + "\n")
            
            print_section("METADATA", f)
            metadata = result.get("metadata", {})
            meta_text = f"""Processing Time: {metadata.get('processing_time', 0):.2f}s
Total Pages: {metadata.get('total_pages', 0)}
Total Chunks: {metadata.get('total_chunks', 0)}
RAG Enabled: {metadata.get('rag_enabled', False)}"""
            print(meta_text, flush=True)
            f.write(meta_text + "\n")
            
            print_section("\u2705 PROCESSING COMPLETE", f)
            f.write(f"\nOutput also saved to: {output_file}\n")
            
        except Exception as e:
            error_msg = f"\n\u274c Error: {e}"
            print(error_msg, flush=True)
            f.write(error_msg + "\n")
            import traceback
            tb = traceback.format_exc()
            print(tb, flush=True)
            f.write(tb + "\n")
            sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n\u26a0 Interrupted")
        sys.exit(1)
