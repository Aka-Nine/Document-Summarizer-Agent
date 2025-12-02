# Test Suite

## Running Tests

### Run All Tests
```bash
pytest tests/
```

### Run Only Unit Tests
```bash
pytest tests/ -m "not integration"
```

### Run Only Integration Tests
```bash
pytest tests/ -m integration
```

### Run Specific Test File
```bash
pytest tests/test_imports.py
```

### Run with Coverage
```bash
pytest tests/ --cov=app --cov-report=html
```

## Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Pytest fixtures
├── test_imports.py          # Import tests
├── test_config.py           # Configuration tests
├── unit/                    # Unit tests
│   └── __init__.py
└── integration/             # Integration tests
    ├── __init__.py
    └── test_connections.py  # External service connections
```

## Test Files

### test_imports.py
Tests that all modules can be imported correctly:
- App imports
- Core imports
- Services imports
- Models imports
- Config imports

### test_config.py
Tests configuration settings:
- Settings loaded
- LLM provider configured
- Cloud provider configured
- RAG enabled

### test_connections.py (Integration)
Tests external service connections:
- Redis connection
- MongoDB connection

## Test Status

✅ **10 tests passing**
⏭️ **1 test skipped** (Redis - requires connection)

## Notes

- Integration tests require external services (MongoDB, Redis)
- Unit tests run without external dependencies
- Use `pytest.ini` for configuration

