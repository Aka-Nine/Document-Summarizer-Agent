# Diagnostic script to check frontend setup
Write-Host "=== Frontend Setup Diagnostic ===" -ForegroundColor Cyan
Write-Host ""

# Check Node.js
Write-Host "Checking Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✓ Node.js installed: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js NOT FOUND" -ForegroundColor Red
    Write-Host "  Please install Node.js from https://nodejs.org/" -ForegroundColor Yellow
    exit 1
}

# Check npm
Write-Host "Checking npm..." -ForegroundColor Yellow
try {
    $npmVersion = npm --version
    Write-Host "✓ npm installed: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ npm NOT FOUND" -ForegroundColor Red
    exit 1
}

# Check if node_modules exists
Write-Host "Checking dependencies..." -ForegroundColor Yellow
if (Test-Path "node_modules") {
    Write-Host "✓ node_modules directory exists" -ForegroundColor Green
    $viteExists = Test-Path "node_modules\vite"
    if ($viteExists) {
        Write-Host "✓ Vite installed" -ForegroundColor Green
    } else {
        Write-Host "✗ Vite not found in node_modules" -ForegroundColor Red
        Write-Host "  Running npm install..." -ForegroundColor Yellow
        npm install
    }
} else {
    Write-Host "✗ node_modules NOT FOUND" -ForegroundColor Red
    Write-Host "  Running npm install..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ npm install FAILED" -ForegroundColor Red
        exit 1
    }
}

# Try to start dev server
Write-Host ""
Write-Host "Starting development server..." -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop" -ForegroundColor Gray
Write-Host ""
npm run dev
