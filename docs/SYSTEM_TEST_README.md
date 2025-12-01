# System Testing and Logging

## Quick Test

Run the comprehensive system test:

```bash
python run_system_tests.py
```

This will test all components:
- ✅ Imports
- ✅ MongoDB connection
- ✅ Redis connection  
- ✅ Cloud Storage
- ✅ LLM configuration
- ✅ Celery configuration
- ✅ FastAPI app

## Log Files

All test results are saved to the `logs/` directory:

- `system_test_YYYYMMDD_HHMMSS.log` - Detailed test log
- `test_results_YYYYMMDD_HHMMSS.json` - Test results in JSON format

## Manual Testing

### Test Individual Components

```bash
# Test MongoDB
python -c "from app.models.mongodb_database import get_database; db = get_database(); db.command('ping'); print('MongoDB OK')"

# Test Redis
python -c "from app.services.redis_service import RedisService; r = RedisService(); r.set_key('test', 'ok'); print('Redis OK')"

# Test Storage
python -c "from app.services.cloud_storage import CloudStorageService; s = CloudStorageService.create(); print('Storage OK')"

# Test API
python -c "from app.api.main import app; print('API OK')"
```

## View Logs

```bash
# View latest log
Get-Content logs\system_test_*.log -Tail 50

# View all logs
Get-ChildItem logs\*.log | Sort-Object LastWriteTime -Descending
```

## Fixed Issues

1. ✅ Removed unused `sqlalchemy.orm.Session` import from `app/api/main.py`
2. ✅ Created comprehensive test suite with logging
3. ✅ Created centralized logging utility in `app/utils/logger.py`

## Next Steps

1. Run `python run_system_tests.py` to verify all components
2. Check log files in `logs/` directory for detailed results
3. Fix any errors reported in the test results
