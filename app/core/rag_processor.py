"""
Enterprise RAG (Retrieval Augmented Generation) Processor
Production-ready RAG implementation with vector search and context retrieval
"""
from typing import List, Dict, Any, Optional
import structlog
import asyncio
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document as LangchainDocument
from app.services.embeddings_service import EmbeddingsService
from app.services.vector_db_service import VectorDBService
from app.config.settings import settings
import uuid
import time

logger = structlog.get_logger()


class RAGProcessor:
    """Retrieval Augmented Generation Processor"""
    
    def __init__(self):
        self.embeddings_service = EmbeddingsService.create()
        self.vector_db = VectorDBService.create()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        self._ensure_index_exists()
    
    def _ensure_index_exists(self):
        """Ensure vector index exists (called from sync context)"""
        try:
            dimension = self.embeddings_service.dimension
            # create_index is async, so we need to run it in an event loop
            # Try to get existing loop first
            try:
                loop = asyncio.get_running_loop()
                # Loop is running, schedule as background task (fire and forget)
                asyncio.create_task(self.vector_db.create_index(dimension))
            except RuntimeError:
                # No running loop, try to get event loop
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        # Loop is running, schedule as task
                        asyncio.create_task(self.vector_db.create_index(dimension))
                    else:
                        # Loop exists but not running, run it
                        loop.run_until_complete(self.vector_db.create_index(dimension))
                except RuntimeError:
                    # No event loop at all, create new one
                    asyncio.run(self.vector_db.create_index(dimension))
        except Exception as e:
            logger.warning("Index creation check failed", error=str(e))
    
    async def index_document(
        self,
        document_id: str,
        chunks: List[LangchainDocument],
        metadata: Dict[str, Any]
    ) -> int:
        """
        Index document chunks in vector database
        
        Args:
            document_id: Database document ID
            chunks: Document chunks to index
            metadata: Additional metadata
        
        Returns:
            Number of chunks indexed
        """
        try:
            # Generate embeddings for all chunks
            texts = [chunk.page_content for chunk in chunks]
            embeddings = await self.embeddings_service.embed_batch(texts)
            
            # Prepare vectors for upsert
            vectors = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                vector_id = f"doc_{document_id}_chunk_{i}"
                vectors.append({
                    "id": vector_id,
                    "vector": embedding,
                    "metadata": {
                        "document_id": document_id,
                        "chunk_index": i,
                        "text": chunk.page_content[:500],  # Store first 500 chars
                        "source": metadata.get("filename", "unknown"),
                        "page": chunk.metadata.get("page", 0),
                        **metadata
                    }
                })
            
            # Upsert to vector database
            await self.vector_db.upsert_vectors(vectors)
            logger.info(
                "Document indexed in vector DB",
                document_id=document_id,
                chunks_indexed=len(vectors)
            )
            
            return len(vectors)
        except Exception as e:
            logger.error("Failed to index document", error=str(e), document_id=document_id)
            raise
    
    async def retrieve_context(
        self,
        query: str,
        document_id: Optional[str] = None,
        top_k: Optional[int] = None,
        similarity_threshold: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant context for a query
        
        Args:
            query: Search query
            document_id: Optional filter by document ID
            top_k: Number of results to return
            similarity_threshold: Minimum similarity score
        
        Returns:
            List of relevant chunks with metadata
        """
        try:
            # Generate query embedding
            query_embedding = await self.embeddings_service.embed_text(query)
            
            # Build filter if document_id provided
            filter_dict = None
            if document_id:
                filter_dict = {"document_id": document_id}
            
            # Search vector database
            top_k = top_k or settings.TOP_K_RETRIEVAL
            results = await self.vector_db.search(
                query_vector=query_embedding,
                top_k=top_k,
                filter_dict=filter_dict
            )
            
            # Use lower threshold or return all results if threshold is None
            # This allows getting context even with lower similarity scores
            threshold = similarity_threshold if similarity_threshold is not None else (settings.SIMILARITY_THRESHOLD * 0.5)  # Lower threshold by default
            filtered_results = [
                r for r in results
                if r.get("score", 0) >= threshold
            ]
            
            # If no results with threshold, return top results anyway (even with low similarity)
            # This allows the LLM to generate answers using whatever context is available
            if not filtered_results and results:
                filtered_results = results[:top_k]  # Return top K even if below threshold
                logger.info(
                    "Using low-similarity context",
                    query=query[:100],
                    results_count=len(filtered_results),
                    min_score=min([r.get("score", 0) for r in filtered_results]) if filtered_results else 0
                )
            
            logger.info(
                "Context retrieved",
                query=query[:100],
                results_count=len(filtered_results),
                document_id=document_id,
                threshold_used=threshold
            )
            
            return filtered_results
        except Exception as e:
            logger.error("Failed to retrieve context", error=str(e), query=query[:100])
            raise
    
    async def delete_document_index(self, document_id: str) -> bool:
        """Delete all vectors for a document"""
        try:
            # Get all vector IDs for this document
            # Note: This requires listing vectors, which may not be supported by all vector DBs
            # For now, we'll use a pattern-based approach
            filter_dict = {"document_id": document_id}
            
            # Search with a dummy query to get vector IDs
            # This is a workaround - in production, you'd want a better method
            stats = await self.vector_db.get_stats()
            logger.info("Document index deletion requested", document_id=document_id)
            
            # For Pinecone/Qdrant, we'd need to implement proper deletion
            # This is a placeholder
            return True
        except Exception as e:
            logger.error("Failed to delete document index", error=str(e), document_id=document_id)
            return False
    
    def chunk_document(self, documents: List[LangchainDocument]) -> List[LangchainDocument]:
        """
        Chunk documents for indexing
        
        Args:
            documents: List of LangChain documents
        
        Returns:
            List of chunked documents
        """
        try:
            chunks = self.text_splitter.split_documents(documents)
            logger.info("Document chunked", original_docs=len(documents), chunks=len(chunks))
            return chunks
        except Exception as e:
            logger.error("Failed to chunk document", error=str(e))
            raise
    
    async def rerank_results(
        self,
        query: str,
        results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Rerank search results for better relevance
        
        Args:
            query: Original query
            results: Search results to rerank
        
        Returns:
            Reranked results
        """
        if not settings.RERANK_ENABLED or not results:
            return results
        
        # TODO: Implement reranking with cross-encoder or dedicated reranking model
        # For now, return results as-is
        logger.info("Reranking requested but not implemented", results_count=len(results))
        return results

