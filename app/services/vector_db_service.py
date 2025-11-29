"""
Enterprise Vector Database Service
Supports Pinecone, Qdrant, Weaviate, Chroma, and OpenSearch
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
import structlog
from app.config.settings import settings, VectorDBProvider
import uuid

logger = structlog.get_logger()


class VectorDBInterface(ABC):
    """Abstract interface for vector database operations"""
    
    @abstractmethod
    async def create_index(self, dimension: int, index_name: Optional[str] = None) -> bool:
        """Create vector index"""
        pass
    
    @abstractmethod
    async def upsert_vectors(self, vectors: List[Dict[str, Any]]) -> bool:
        """Upsert vectors with metadata"""
        pass
    
    @abstractmethod
    async def search(self, query_vector: List[float], top_k: int = 5, filter_dict: Optional[Dict] = None) -> List[Dict]:
        """Search similar vectors"""
        pass
    
    @abstractmethod
    async def delete_vectors(self, vector_ids: List[str]) -> bool:
        """Delete vectors by IDs"""
        pass
    
    @abstractmethod
    async def get_stats(self) -> Dict[str, Any]:
        """Get index statistics"""
        pass


class PineconeVectorDBService(VectorDBInterface):
    """Pinecone Vector Database Service"""
    
    def __init__(self):
        try:
            import pinecone
            if not settings.PINECONE_API_KEY:
                raise ValueError("PINECONE_API_KEY is required")
            
            pinecone.init(
                api_key=settings.PINECONE_API_KEY,
                environment=settings.PINECONE_ENVIRONMENT
            )
            self.index_name = settings.PINECONE_INDEX_NAME or settings.VECTOR_DB_INDEX_NAME
            self.pinecone = pinecone
        except ImportError:
            raise ImportError("pinecone-client not installed. Install with: pip install pinecone-client")
    
    async def create_index(self, dimension: int, index_name: Optional[str] = None) -> bool:
        """Create Pinecone index"""
        try:
            index_name = index_name or self.index_name
            if index_name not in self.pinecone.list_indexes():
                self.pinecone.create_index(
                    name=index_name,
                    dimension=dimension,
                    metric="cosine"
                )
                logger.info("Pinecone index created", index=index_name)
            return True
        except Exception as e:
            logger.error("Failed to create Pinecone index", error=str(e))
            raise
    
    async def upsert_vectors(self, vectors: List[Dict[str, Any]]) -> bool:
        """Upsert vectors to Pinecone"""
        try:
            index = self.pinecone.Index(self.index_name)
            # Format: [(id, vector, metadata), ...]
            formatted_vectors = [
                (
                    v.get("id", str(uuid.uuid4())),
                    v["vector"],
                    v.get("metadata", {})
                )
                for v in vectors
            ]
            index.upsert(vectors=formatted_vectors)
            logger.info("Vectors upserted to Pinecone", count=len(vectors))
            return True
        except Exception as e:
            logger.error("Pinecone upsert failed", error=str(e))
            raise
    
    async def search(self, query_vector: List[float], top_k: int = 5, filter_dict: Optional[Dict] = None) -> List[Dict]:
        """Search Pinecone index"""
        try:
            index = self.pinecone.Index(self.index_name)
            results = index.query(
                vector=query_vector,
                top_k=top_k,
                include_metadata=True,
                filter=filter_dict
            )
            return [
                {
                    "id": match.id,
                    "score": match.score,
                    "metadata": match.metadata
                }
                for match in results.matches
            ]
        except Exception as e:
            logger.error("Pinecone search failed", error=str(e))
            raise
    
    async def delete_vectors(self, vector_ids: List[str]) -> bool:
        """Delete vectors from Pinecone"""
        try:
            index = self.pinecone.Index(self.index_name)
            index.delete(ids=vector_ids)
            logger.info("Vectors deleted from Pinecone", count=len(vector_ids))
            return True
        except Exception as e:
            logger.error("Pinecone delete failed", error=str(e))
            raise
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get Pinecone index stats"""
        try:
            index = self.pinecone.Index(self.index_name)
            stats = index.describe_index_stats()
            return {
                "total_vectors": stats.total_vector_count,
                "dimension": stats.dimension,
                "index_fullness": stats.index_fullness
            }
        except Exception as e:
            logger.error("Failed to get Pinecone stats", error=str(e))
            raise


class QdrantVectorDBService(VectorDBInterface):
    """Qdrant Vector Database Service"""
    
    def __init__(self):
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.models import Distance, VectorParams
            
            if not settings.QDRANT_URL:
                raise ValueError("QDRANT_URL is required")
            
            self.client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY
            )
            self.collection_name = settings.QDRANT_COLLECTION_NAME or settings.VECTOR_DB_INDEX_NAME
            self.VectorParams = VectorParams
            self.Distance = Distance
        except ImportError:
            raise ImportError("qdrant-client not installed. Install with: pip install qdrant-client")
    
    async def create_index(self, dimension: int, index_name: Optional[str] = None) -> bool:
        """Create Qdrant collection"""
        try:
            collection_name = index_name or self.collection_name
            collections = self.client.get_collections().collections
            if not any(c.name == collection_name for c in collections):
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=self.VectorParams(
                        size=dimension,
                        distance=self.Distance.COSINE
                    )
                )
                logger.info("Qdrant collection created", collection=collection_name)
            return True
        except Exception as e:
            logger.error("Failed to create Qdrant collection", error=str(e))
            raise
    
    async def upsert_vectors(self, vectors: List[Dict[str, Any]]) -> bool:
        """Upsert vectors to Qdrant"""
        try:
            from qdrant_client.models import PointStruct
            
            points = [
                PointStruct(
                    id=v.get("id", str(uuid.uuid4())),
                    vector=v["vector"],
                    payload=v.get("metadata", {})
                )
                for v in vectors
            ]
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            logger.info("Vectors upserted to Qdrant", count=len(vectors))
            return True
        except Exception as e:
            logger.error("Qdrant upsert failed", error=str(e))
            raise
    
    async def search(self, query_vector: List[float], top_k: int = 5, filter_dict: Optional[Dict] = None) -> List[Dict]:
        """Search Qdrant collection"""
        try:
            from qdrant_client.models import Filter, FieldCondition, MatchValue
            
            search_filter = None
            if filter_dict:
                conditions = [
                    FieldCondition(key=k, match=MatchValue(value=v))
                    for k, v in filter_dict.items()
                ]
                search_filter = Filter(must=conditions)
            
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k,
                query_filter=search_filter
            )
            return [
                {
                    "id": result.id,
                    "score": result.score,
                    "metadata": result.payload
                }
                for result in results
            ]
        except Exception as e:
            logger.error("Qdrant search failed", error=str(e))
            raise
    
    async def delete_vectors(self, vector_ids: List[str]) -> bool:
        """Delete vectors from Qdrant"""
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=vector_ids
            )
            logger.info("Vectors deleted from Qdrant", count=len(vector_ids))
            return True
        except Exception as e:
            logger.error("Qdrant delete failed", error=str(e))
            raise
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get Qdrant collection stats"""
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                "total_vectors": info.points_count,
                "vectors_count": info.points_count,
                "indexed_vectors_count": info.indexed_vectors_count
            }
        except Exception as e:
            logger.error("Failed to get Qdrant stats", error=str(e))
            raise


class ChromaVectorDBService(VectorDBInterface):
    """Chroma Vector Database Service (Local)"""
    
    def __init__(self):
        try:
            import chromadb
            from chromadb.config import Settings as ChromaSettings
            
            persist_dir = settings.CHROMA_PERSIST_DIR or "./chroma_db"
            self.client = chromadb.PersistentClient(
                path=persist_dir,
                settings=ChromaSettings(anonymized_telemetry=False)
            )
            self.collection_name = settings.VECTOR_DB_INDEX_NAME or "document-intelligence"
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("Chroma vector DB initialized", collection=self.collection_name, persist_dir=persist_dir)
        except ImportError:
            raise ImportError("chromadb is required. Install with: pip install chromadb")
        except Exception as e:
            logger.error("Chroma initialization failed", error=str(e))
            raise
    
    async def create_index(self, dimension: int, index_name: Optional[str] = None) -> bool:
        """Chroma creates collection automatically, just verify it exists"""
        try:
            if index_name:
                self.collection = self.client.get_or_create_collection(name=index_name)
            logger.info("Chroma index ready", collection=self.collection.name)
            return True
        except Exception as e:
            logger.error("Chroma index creation failed", error=str(e))
            return False
    
    async def upsert_vectors(self, vectors: List[Dict[str, Any]]) -> bool:
        """Upsert vectors to Chroma"""
        try:
            ids = [v.get("id", str(uuid.uuid4())) for v in vectors]
            embeddings = [v["vector"] for v in vectors]
            metadatas = [v.get("metadata", {}) for v in vectors]
            documents = [v.get("text", "") for v in vectors]
            
            self.collection.upsert(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas,
                documents=documents
            )
            logger.info("Vectors upserted to Chroma", count=len(vectors))
            return True
        except Exception as e:
            logger.error("Chroma upsert failed", error=str(e))
            raise
    
    async def search(self, query_vector: List[float], top_k: int = 5, filter_dict: Optional[Dict] = None) -> List[Dict]:
        """Search Chroma collection"""
        try:
            where = filter_dict if filter_dict else None
            results = self.collection.query(
                query_embeddings=[query_vector],
                n_results=top_k,
                where=where
            )
            
            # Format results
            formatted_results = []
            if results["ids"] and len(results["ids"][0]) > 0:
                for i in range(len(results["ids"][0])):
                    formatted_results.append({
                        "id": results["ids"][0][i],
                        "score": 1 - results["distances"][0][i] if "distances" in results else 0.0,
                        "metadata": results["metadatas"][0][i] if results.get("metadatas") else {},
                        "text": results["documents"][0][i] if results.get("documents") else ""
                    })
            
            return formatted_results
        except Exception as e:
            logger.error("Chroma search failed", error=str(e))
            raise
    
    async def delete_vectors(self, vector_ids: List[str]) -> bool:
        """Delete vectors from Chroma"""
        try:
            self.collection.delete(ids=vector_ids)
            logger.info("Vectors deleted from Chroma", count=len(vector_ids))
            return True
        except Exception as e:
            logger.error("Chroma delete failed", error=str(e))
            raise
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get Chroma collection stats"""
        try:
            count = self.collection.count()
            return {
                "total_vectors": count,
                "vectors_count": count,
                "indexed_vectors_count": count
            }
        except Exception as e:
            logger.error("Failed to get Chroma stats", error=str(e))
            raise


class VectorDBService:
    """Factory for vector database services"""
    
    @staticmethod
    def create() -> VectorDBInterface:
        """Create appropriate vector database service"""
        provider = settings.VECTOR_DB_PROVIDER
        
        if provider == VectorDBProvider.PINECONE:
            return PineconeVectorDBService()
        elif provider == VectorDBProvider.QDRANT:
            return QdrantVectorDBService()
        elif provider == VectorDBProvider.WEAVIATE:
            raise NotImplementedError("Weaviate not yet implemented")
        elif provider == VectorDBProvider.CHROMA:
            return ChromaVectorDBService()
        elif provider == VectorDBProvider.OPENSEARCH:
            raise NotImplementedError("OpenSearch not yet implemented")
        else:
            raise ValueError(f"Unsupported vector DB provider: {provider}")

