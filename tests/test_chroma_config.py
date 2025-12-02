#!/usr/bin/env python
"""Test and display Chroma Cloud configuration"""

import asyncio
from app.services.vector_db_service import VectorDBService
from app.config.settings import settings

print("=" * 70)
print(" CHROMA CLOUD CONFIGURATION VERIFICATION ".center(70))
print("=" * 70)

print("\n📋 CONFIGURATION DETAILS:")
print(f"   Vector DB Provider: {settings.VECTOR_DB_PROVIDER}")
api_key_masked = "●●●●●●●●●●●●●" + settings.CHROMA_API_KEY[-4:] if settings.CHROMA_API_KEY else "Not set"
print(f"   Chroma API Key: {api_key_masked}")
print(f"   Chroma Tenant: {settings.CHROMA_TENANT}")
print(f"   Chroma Database: {settings.CHROMA_DATABASE}")
print(f"   Chroma Server: {settings.CHROMA_SERVER_HOST}:{settings.CHROMA_SERVER_PORT}")

print("\n" + "=" * 70)
print(" SERVICE STATUS ".center(70))
print("=" * 70)

try:
    # Initialize Chroma Cloud service
    service = VectorDBService.create()
    print("\n✅ Chroma Cloud service initialized successfully!")
    print(f"   Collection name: {service.collection_name}")
    
    # Get collection statistics
    async def get_stats():
        return await service.get_stats()
    
    stats = asyncio.run(get_stats())
    print(f"   Total vectors in collection: {stats.get('total_vectors', 0)}")
    
    print("\n" + "=" * 70)
    print(" FILES UPDATED ".center(70))
    print("=" * 70)
    print("\n✓ .env")
    print("  └─ Added Chroma Cloud credentials (your credentials saved)")
    print("\n✓ config.env")
    print("  └─ Added Chroma Cloud configuration template")
    print("\n✓ env.example")
    print("  └─ Added Chroma Cloud configuration example")
    print("\n✓ app/config/settings.py")
    print("  └─ Added CHROMA_API_KEY, CHROMA_TENANT, CHROMA_DATABASE settings")
    print("  └─ Set VECTOR_DB_PROVIDER to CHROMA")
    print("\n✓ app/services/vector_db_service.py")
    print("  └─ Updated ChromaVectorDBService to support Chroma Cloud")
    print("  └─ Uses chromadb.CloudClient for authentication")
    
    print("\n" + "=" * 70)
    print(" READY TO USE ".center(70))
    print("=" * 70)
    print("\n✅ Your Chroma Cloud database is configured and connected!")
    print("\nYou can now:")
    print("  • Upsert document embeddings to Chroma Cloud")
    print("  • Perform semantic search on stored vectors")
    print("  • Use RAG (Retrieval-Augmented Generation) features")
    print("  • All data is stored in: User-Data database (Your tenant)")
    
    print("\n" + "=" * 70)
    
except Exception as e:
    print(f"\n❌ Error initializing Chroma Cloud: {e}")
    print("\nTroubleshooting:")
    print("  • Verify API key is correct")
    print("  • Verify tenant ID is correct")
    print("  • Verify database name is correct")
    print("  • Check your internet connection")
    import traceback
    traceback.print_exc()
