#!/usr/bin/env python3
"""Check recent documents in MongoDB and show processing status.

Run from repository root: `python scripts/check_recent_documents.py`
"""
import json
import sys

try:
    from app.models.mongodb_database import get_documents_collection, DocumentModel
except Exception:
    print("Failed to import app.models.mongodb_database. Ensure project is on PYTHONPATH.")
    raise


def main():
    try:
        coll = get_documents_collection()
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        sys.exit(2)

    docs = list(coll.find().sort("created_at", -1).limit(20))

    out = []
    for d in docs:
        try:
            out.append(DocumentModel.to_dict(d))
        except Exception:
            # Best-effort formatting
            out.append({
                "id": str(d.get("_id")),
                "filename": d.get("filename"),
                "status": d.get("status"),
                "created_at": str(d.get("created_at")),
                "processed_at": str(d.get("processed_at")),
                "user_id": str(d.get("user_id", "")),
            })

    print(json.dumps(out, default=str, indent=2))


if __name__ == "__main__":
    main()
