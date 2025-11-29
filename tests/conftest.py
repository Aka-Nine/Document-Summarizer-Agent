"""
Pytest configuration and fixtures
"""
import pytest
import os
from pathlib import Path


@pytest.fixture(scope="session")
def test_data_dir():
    """Fixture for test data directory"""
    test_dir = Path(__file__).parent / "test_data"
    test_dir.mkdir(exist_ok=True)
    return test_dir


@pytest.fixture(scope="session")
def sample_text():
    """Fixture for sample text"""
    return """
    This is a sample document for testing purposes.
    It contains multiple sentences and paragraphs.
    The document processing system should be able to handle this text.
    """


@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch):
    """Setup test environment variables"""
    # Set test environment variables if not already set
    if "TESTING" not in os.environ:
        monkeypatch.setenv("TESTING", "true")

