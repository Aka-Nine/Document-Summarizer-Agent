"""
Test configuration settings
"""
import pytest
from app.config.settings import settings


def test_settings_loaded():
    """Test that settings are loaded"""
    assert settings is not None
    assert hasattr(settings, 'SECRET_KEY')
    assert hasattr(settings, 'MONGODB_URL')
    assert hasattr(settings, 'REDIS_URL')


def test_llm_provider():
    """Test LLM provider is set"""
    assert settings.LLM_PROVIDER is not None
    assert settings.LLM_PROVIDER in ['gemini', 'groq', 'openai', 'anthropic']


def test_cloud_provider():
    """Test cloud provider is set"""
    assert settings.CLOUD_PROVIDER is not None
    assert settings.CLOUD_PROVIDER in ['filesystem', 'aws', 'azure', 'gcp', 'minio']


def test_rag_enabled():
    """Test RAG configuration"""
    assert hasattr(settings, 'RAG_ENABLED')
    assert isinstance(settings.RAG_ENABLED, bool)

