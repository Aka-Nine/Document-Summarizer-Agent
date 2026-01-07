# Start Celery Worker Script for Windows PowerShell
# This script starts the Celery worker for document processing

Write-Host "=" * 70
Write-Host " Starting Celery Worker ".PadLeft(40)
Write-Host "=" * 70

# Set environment variables
$env:ENV_FILE_PATH = "d:\doc-summ-agent\config\.env"
$env:PYTHONPATH = "d:\doc-summ-agent"

# Change to project directory
Set-Location "d:\doc-summ-agent"

# Activate virtual environment if it exists
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Green
    .\venv\Scripts\Activate.ps1
}

# Check if Celery is installed
Write-Host "Checking Celery installation..." -ForegroundColor Yellow
try {
    $celeryVersion = python -c "import celery; print(celery.__version__)" 2>&1
    Write-Host "Celery version: $celeryVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Celery not installed. Install with: pip install celery" -ForegroundColor Red
    exit 1
}

# Check Redis connection
Write-Host "Checking Redis connection..." -ForegroundColor Yellow
try {
    python -c "from app.services.redis_service import RedisService; RedisService(); print('Redis connected')" 2>&1 | Out-Null
    Write-Host "Redis connection: OK" -ForegroundColor Green
} catch {
    Write-Host "WARNING: Redis connection failed. Worker may not work properly." -ForegroundColor Yellow
}

# Start Celery worker using the script (which loads env vars properly)
Write-Host ""
Write-Host "Starting Celery worker..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the worker" -ForegroundColor Yellow
Write-Host ""

# Load .env file first, then use celery command directly
# This is more reliable than using worker_main()
Write-Host "Loading environment variables..." -ForegroundColor Yellow
python -c "from dotenv import load_dotenv; import os; load_dotenv('config/.env', override=True); os.environ['ENV_FILE_PATH'] = 'd:/doc-summ-agent/config/.env'"

# Start Celery worker with standard command
# Use --pool=solo for Windows compatibility (avoids multiprocessing issues)
Write-Host "Starting Celery worker (Windows: using solo pool)..." -ForegroundColor Green
celery -A app.tasks.celery_tasks worker --loglevel=info --pool=solo

