"""
Test that all imports work correctly
"""
import pytest


def test_app_imports():
    """Test that main app imports work"""
    from app.api.main import app
    assert app is not None
    assert len(app.routes) > 0


def test_core_imports():
    """Test that core modules import"""
    from app.core.enterprise_document_processor import EnterpriseDocumentProcessor
    from app.core.rag_processor import RAGProcessor
    assert EnterpriseDocumentProcessor is not None
    assert RAGProcessor is not None


def test_services_imports():
    """Test that services import"""
    from app.services.cloud_storage import CloudStorageService
    from app.services.redis_service import RedisService
    from app.services.embeddings_service import EmbeddingsService
    from app.services.vector_db_service import VectorDBService
    assert CloudStorageService is not None
    assert RedisService is not None
    assert EmbeddingsService is not None
    assert VectorDBService is not None


def test_models_imports():
    """Test that models import"""
    from app.models.mongodb_database import (
        UserModel, DocumentModel, DocumentQueryModel
    )
    assert UserModel is not None
    assert DocumentModel is not None
    assert DocumentQueryModel is not None


def test_config_imports():
    """Test that config imports"""
    from app.config.settings import settings
    assert settings is not None

