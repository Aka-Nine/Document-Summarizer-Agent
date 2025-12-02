"""
Enterprise Embeddings Service
Supports OpenAI, Cohere, HuggingFace, AWS Bedrock, and Groq
"""
from abc import ABC, abstractmethod
from typing import List, Optional
import structlog
from app.config.settings import settings, EmbeddingProvider
import openai
from openai import OpenAI
try:
    import cohere
except ImportError:
    cohere = None
try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None
import boto3
try:
    from groq import Groq
except ImportError:
    Groq = None

logger = structlog.get_logger()


class EmbeddingsInterface(ABC):
    """Abstract interface for embeddings"""
    
    @abstractmethod
    async def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        pass
    
    @abstractmethod
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        pass
    
    @property
    def dimension(self) -> int:
        """Return embedding dimension"""
        pass


class OpenAIEmbeddingsService(EmbeddingsInterface):
    """OpenAI Embeddings Service"""
    
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required for OpenAI embeddings")
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY, organization=settings.OPENAI_ORG_ID)
        self.model = settings.EMBEDDING_MODEL
        self.dimension = settings.EMBEDDING_DIMENSION
    
    async def embed_text(self, text: str) -> List[float]:
        """Generate embedding using OpenAI"""
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error("OpenAI embedding failed", error=str(e))
            raise
    
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for batch"""
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=texts
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            logger.error("OpenAI batch embedding failed", error=str(e))
            raise


class CohereEmbeddingsService(EmbeddingsInterface):
    """Cohere Embeddings Service"""
    
    def __init__(self):
        if not settings.COHERE_API_KEY:
            raise ValueError("COHERE_API_KEY is required for Cohere embeddings")
        self.client = cohere.Client(settings.COHERE_API_KEY)
        self.dimension = 1024  # Cohere default
    
    async def embed_text(self, text: str) -> List[float]:
        """Generate embedding using Cohere"""
        try:
            response = self.client.embed(texts=[text], model="embed-english-v3.0")
            return response.embeddings[0]
        except Exception as e:
            logger.error("Cohere embedding failed", error=str(e))
            raise
    
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for batch"""
        try:
            response = self.client.embed(texts=texts, model="embed-english-v3.0")
            return response.embeddings
        except Exception as e:
            logger.error("Cohere batch embedding failed", error=str(e))
            raise


class HuggingFaceEmbeddingsService(EmbeddingsInterface):
    """HuggingFace Embeddings Service (local model)"""
    
    def __init__(self):
        if SentenceTransformer is None:
            raise ImportError("sentence-transformers is required. Install with: pip install sentence-transformers")
        self.model_name = settings.HUGGINGFACE_MODEL_NAME
        self.model = SentenceTransformer(self.model_name)
        self._dimension = self.model.get_sentence_embedding_dimension()
    
    @property
    def dimension(self) -> int:
        """Return embedding dimension"""
        return self._dimension
    
    async def embed_text(self, text: str) -> List[float]:
        """Generate embedding using HuggingFace"""
        try:
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding.tolist()
        except Exception as e:
            logger.error("HuggingFace embedding failed", error=str(e))
            raise
    
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for batch"""
        try:
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            return embeddings.tolist()
        except Exception as e:
            logger.error("HuggingFace batch embedding failed", error=str(e))
            raise


class AWSBedrockEmbeddingsService(EmbeddingsInterface):
    """AWS Bedrock Embeddings Service"""
    
    def __init__(self):
        if not settings.AWS_REGION:
            raise ValueError("AWS_REGION is required for AWS Bedrock")
        self.bedrock_runtime = boto3.client(
            'bedrock-runtime',
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        self.model_id = settings.AWS_BEDROCK_MODEL_ID
        self.dimension = 1536  # Titan default
    
    async def embed_text(self, text: str) -> List[float]:
        """Generate embedding using AWS Bedrock"""
        try:
            import json
            body = json.dumps({"inputText": text})
            response = self.bedrock_runtime.invoke_model(
                modelId=self.model_id,
                body=body
            )
            response_body = json.loads(response['body'].read())
            return response_body['embedding']
        except Exception as e:
            logger.error("AWS Bedrock embedding failed", error=str(e))
            raise
    
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for batch"""
        embeddings = []
        for text in texts:
            embedding = await self.embed_text(text)
            embeddings.append(embedding)
        return embeddings


class EmbeddingsService:
    """Factory for embeddings services"""
    
    @staticmethod
    def create() -> EmbeddingsInterface:
        """Create appropriate embeddings service"""
        provider = settings.EMBEDDING_PROVIDER
        
        if provider == EmbeddingProvider.OPENAI:
            return OpenAIEmbeddingsService()
        elif provider == EmbeddingProvider.COHERE:
            return CohereEmbeddingsService()
        elif provider == EmbeddingProvider.HUGGINGFACE:
            return HuggingFaceEmbeddingsService()
        elif provider == EmbeddingProvider.AWS_BEDROCK:
            return AWSBedrockEmbeddingsService()
        else:
            raise ValueError(f"Unsupported embedding provider: {provider}")

