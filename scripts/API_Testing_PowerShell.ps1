# ============================================================================
# API TESTING WITH POWERSHELL - For Windows Users
# ============================================================================
# Run these commands in PowerShell to test the API
# Make sure the FastAPI server is running on http://localhost:8000

# Configuration
$API_BASE = "http://localhost:8000"
$API_V1 = "$API_BASE/api/v1"
$AUTH_TOKEN = ""
$DOCUMENT_ID = ""

# ============================================================================
# FUNCTION: Make API Request
# ============================================================================

function Invoke-APIRequest {
    param(
        [string]$Method = "GET",
        [string]$Endpoint,
        [hashtable]$Headers,
        [psobject]$Body
    )
    
    $params = @{
        Method = $Method
        Uri = $Endpoint
        ContentType = "application/json"
    }
    
    if ($Headers) {
        $params.Headers = $Headers
    }
    
    if ($Body) {
        $params.Body = $Body | ConvertTo-Json
    }
    
    try {
        $response = Invoke-RestMethod @params
        return $response
    } catch {
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "Response: $($_.Exception.Response.Content)" -ForegroundColor Red
        return $null
    }
}

# ============================================================================
# TEST 1: HEALTH CHECK
# ============================================================================

function Test-HealthCheck {
    Write-Host "`n=== Testing Health Check ===" -ForegroundColor Cyan
    
    $response = Invoke-RestMethod -Uri "$API_BASE/health" -Method Get
    Write-Host "Status: $($response.status)" -ForegroundColor Green
    Write-Host "Full Response:" -ForegroundColor Cyan
    $response | ConvertTo-Json | Write-Host
    
    if ($response.status -eq "healthy") {
        Write-Host "✅ API is healthy!" -ForegroundColor Green
        return $true
    } else {
        Write-Host "❌ API is not healthy" -ForegroundColor Red
        return $false
    }
}

# ============================================================================
# TEST 2: USER REGISTRATION
# ============================================================================

function Test-UserRegistration {
    Write-Host "`n=== Testing User Registration ===" -ForegroundColor Cyan
    
    $userData = @{
        username = "testuser@example.com"
        password = "TestPassword123!"
        full_name = "Test User"
    } | ConvertTo-Json
    
    Write-Host "Registering user..." -ForegroundColor Yellow
    
    try {
        $response = Invoke-RestMethod `
            -Uri "$API_V1/auth/register" `
            -Method Post `
            -ContentType "application/json" `
            -Body $userData
        
        Write-Host "User registered successfully!" -ForegroundColor Green
        Write-Host "User ID: $($response.user_id)" -ForegroundColor Green
        Write-Host "Full Response:" -ForegroundColor Cyan
        $response | ConvertTo-Json | Write-Host
        return $true
    } catch {
        if ($_.Exception.Response.StatusCode -eq 409) {
            Write-Host "User already exists (409). That's OK for testing." -ForegroundColor Yellow
            return $true
        } else {
            Write-Host "Registration failed: $($_.Exception.Message)" -ForegroundColor Red
            return $false
        }
    }
}

# ============================================================================
# TEST 3: USER LOGIN
# ============================================================================

function Test-UserLogin {
    Write-Host "`n=== Testing User Login ===" -ForegroundColor Cyan
    
    $loginData = @{
        username = "testuser@example.com"
        password = "TestPassword123!"
    } | ConvertTo-Json
    
    Write-Host "Logging in..." -ForegroundColor Yellow
    
    try {
        $response = Invoke-RestMethod `
            -Uri "$API_V1/auth/login" `
            -Method Post `
            -ContentType "application/json" `
            -Body $loginData
        
        $global:AUTH_TOKEN = $response.access_token -or $response.token
        
        Write-Host "Login successful!" -ForegroundColor Green
        Write-Host "Token: $($global:AUTH_TOKEN.Substring(0, 20))..." -ForegroundColor Green
        Write-Host "Full Response:" -ForegroundColor Cyan
        $response | ConvertTo-Json | Write-Host
        return $true
    } catch {
        Write-Host "Login failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# ============================================================================
# TEST 4: UPLOAD DOCUMENT
# ============================================================================

function Test-DocumentUpload {
    Write-Host "`n=== Testing Document Upload ===" -ForegroundColor Cyan
    
    if (-not $global:AUTH_TOKEN) {
        Write-Host "❌ No auth token. Login first." -ForegroundColor Red
        return $false
    }
    
    # Create test file
    $testFile = "test_document.txt"
    $content = "This is a test document for API testing. " * 50
    Set-Content -Path $testFile -Value $content
    Write-Host "Created test file: $testFile" -ForegroundColor Yellow
    
    Write-Host "Uploading document..." -ForegroundColor Yellow
    
    try {
        $headers = @{
            "Authorization" = "Bearer $global:AUTH_TOKEN"
        }
        
        # Use System.Net.Http.MultipartFormDataContent for file upload
        $filePath = (Get-Item $testFile).FullName
        $fileName = Split-Path $filePath -Leaf
        
        $fileBytes = [System.IO.File]::ReadAllBytes($filePath)
        
        $multipartContent = [System.Net.Http.MultipartFormDataContent]::new()
        $fileStream = [System.IO.FileStream]::new($filePath, [System.IO.FileMode]::Open)
        $fileContent = [System.Net.Http.StreamContent]::new($fileStream)
        $multipartContent.Add($fileContent, "file", $fileName)
        $multipartContent.Add([System.Net.Http.StringContent]::new("Test Document"), "title")
        $multipartContent.Add([System.Net.Http.StringContent]::new("Test document for API"), "description")
        
        $httpClient = [System.Net.Http.HttpClient]::new()
        $httpClient.DefaultRequestHeaders.Authorization = `
            [System.Net.Http.Headers.AuthenticationHeaderValue]::new("Bearer", $global:AUTH_TOKEN)
        
        $response = $httpClient.PostAsync("$API_V1/documents/upload", $multipartContent).Result
        $content = $response.Content.ReadAsStringAsync().Result
        $responseObj = $content | ConvertFrom-Json
        
        $global:DOCUMENT_ID = $responseObj.document_id
        
        Write-Host "Document uploaded successfully!" -ForegroundColor Green
        Write-Host "Document ID: $global:DOCUMENT_ID" -ForegroundColor Green
        Write-Host "Status: $($responseObj.status)" -ForegroundColor Green
        Write-Host "Full Response:" -ForegroundColor Cyan
        $responseObj | ConvertTo-Json | Write-Host
        return $true
    } catch {
        Write-Host "Upload failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# ============================================================================
# TEST 5: GET DOCUMENT
# ============================================================================

function Test-GetDocument {
    Write-Host "`n=== Testing Get Document ===" -ForegroundColor Cyan
    
    if (-not $global:AUTH_TOKEN) {
        Write-Host "❌ No auth token. Login first." -ForegroundColor Red
        return $false
    }
    
    if (-not $global:DOCUMENT_ID) {
        Write-Host "❌ No document ID. Upload first." -ForegroundColor Red
        return $false
    }
    
    Write-Host "Getting document details..." -ForegroundColor Yellow
    
    try {
        $headers = @{
            "Authorization" = "Bearer $global:AUTH_TOKEN"
        }
        
        $response = Invoke-RestMethod `
            -Uri "$API_V1/documents/$global:DOCUMENT_ID" `
            -Method Get `
            -Headers $headers
        
        Write-Host "Document retrieved!" -ForegroundColor Green
        Write-Host "Full Response:" -ForegroundColor Cyan
        $response | ConvertTo-Json | Write-Host
        return $true
    } catch {
        Write-Host "Get document failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# ============================================================================
# TEST 6: LIST DOCUMENTS
# ============================================================================

function Test-ListDocuments {
    Write-Host "`n=== Testing List Documents ===" -ForegroundColor Cyan
    
    if (-not $global:AUTH_TOKEN) {
        Write-Host "❌ No auth token. Login first." -ForegroundColor Red
        return $false
    }
    
    Write-Host "Listing documents..." -ForegroundColor Yellow
    
    try {
        $headers = @{
            "Authorization" = "Bearer $global:AUTH_TOKEN"
        }
        
        $response = Invoke-RestMethod `
            -Uri "$API_V1/documents?page=1&page_size=10" `
            -Method Get `
            -Headers $headers
        
        Write-Host "Documents listed!" -ForegroundColor Green
        Write-Host "Count: $($response.documents.Length)" -ForegroundColor Green
        Write-Host "Full Response:" -ForegroundColor Cyan
        $response | ConvertTo-Json -Depth 3 | Write-Host
        return $true
    } catch {
        Write-Host "List documents failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# ============================================================================
# TEST 7: SEARCH
# ============================================================================

function Test-Search {
    param(
        [string]$Query = "test"
    )
    
    Write-Host "`n=== Testing Semantic Search ===" -ForegroundColor Cyan
    
    if (-not $global:AUTH_TOKEN) {
        Write-Host "❌ No auth token. Login first." -ForegroundColor Red
        return $false
    }
    
    Write-Host "Searching for: $Query" -ForegroundColor Yellow
    
    try {
        $headers = @{
            "Authorization" = "Bearer $global:AUTH_TOKEN"
        }
        
        $response = Invoke-RestMethod `
            -Uri "$API_V1/search?q=$Query&top_k=5" `
            -Method Get `
            -Headers $headers
        
        Write-Host "Search completed!" -ForegroundColor Green
        Write-Host "Results: $($response.results.Length)" -ForegroundColor Green
        Write-Host "Full Response:" -ForegroundColor Cyan
        $response | ConvertTo-Json -Depth 3 | Write-Host
        return $true
    } catch {
        Write-Host "Search failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# ============================================================================
# TEST 8: CHAT
# ============================================================================

function Test-Chat {
    param(
        [string]$Message = "What is this document about?"
    )
    
    Write-Host "`n=== Testing Chat (RAG) ===" -ForegroundColor Cyan
    
    if (-not $global:AUTH_TOKEN) {
        Write-Host "❌ No auth token. Login first." -ForegroundColor Red
        return $false
    }
    
    if (-not $global:DOCUMENT_ID) {
        Write-Host "❌ No document ID. Upload first." -ForegroundColor Red
        return $false
    }
    
    Write-Host "Sending message: $Message" -ForegroundColor Yellow
    
    $chatData = @{
        message = $Message
        document_id = $global:DOCUMENT_ID
    } | ConvertTo-Json
    
    try {
        $headers = @{
            "Authorization" = "Bearer $global:AUTH_TOKEN"
        }
        
        $response = Invoke-RestMethod `
            -Uri "$API_V1/chat" `
            -Method Post `
            -ContentType "application/json" `
            -Headers $headers `
            -Body $chatData
        
        Write-Host "Chat response received!" -ForegroundColor Green
        Write-Host "Full Response:" -ForegroundColor Cyan
        $response | ConvertTo-Json -Depth 3 | Write-Host
        return $true
    } catch {
        Write-Host "Chat failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# ============================================================================
# TEST 9: SUMMARIZE
# ============================================================================

function Test-Summarize {
    Write-Host "`n=== Testing Summarize ===" -ForegroundColor Cyan
    
    if (-not $global:AUTH_TOKEN) {
        Write-Host "❌ No auth token. Login first." -ForegroundColor Red
        return $false
    }
    
    if (-not $global:DOCUMENT_ID) {
        Write-Host "❌ No document ID. Upload first." -ForegroundColor Red
        return $false
    }
    
    Write-Host "Generating summary..." -ForegroundColor Yellow
    
    $summaryData = @{
        document_id = $global:DOCUMENT_ID
        summary_length = "medium"
    } | ConvertTo-Json
    
    try {
        $headers = @{
            "Authorization" = "Bearer $global:AUTH_TOKEN"
        }
        
        $response = Invoke-RestMethod `
            -Uri "$API_V1/summarize" `
            -Method Post `
            -ContentType "application/json" `
            -Headers $headers `
            -Body $summaryData
        
        Write-Host "Summary generated!" -ForegroundColor Green
        Write-Host "Full Response:" -ForegroundColor Cyan
        $response | ConvertTo-Json -Depth 3 | Write-Host
        return $true
    } catch {
        Write-Host "Summarize failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# ============================================================================
# MAIN: RUN ALL TESTS
# ============================================================================

function Run-AllTests {
    Write-Host "`n" + ("="*70) -ForegroundColor Cyan
    Write-Host "ENTERPRISE DOCUMENT INTELLIGENCE PLATFORM - API TEST SUITE".PadRight(70).Substring(0, 70) -ForegroundColor Cyan
    Write-Host ("="*70) -ForegroundColor Cyan
    Write-Host "Target: $API_BASE`n" -ForegroundColor Yellow
    
    # Run tests in sequence
    Test-HealthCheck
    Start-Sleep -Seconds 1
    
    Test-UserRegistration
    Start-Sleep -Seconds 1
    
    Test-UserLogin
    Start-Sleep -Seconds 1
    
    Test-DocumentUpload
    Start-Sleep -Seconds 3  # Wait for processing
    
    Test-GetDocument
    Start-Sleep -Seconds 1
    
    Test-ListDocuments
    Start-Sleep -Seconds 1
    
    Test-Search
    Start-Sleep -Seconds 1
    
    if ($global:DOCUMENT_ID) {
        Test-Chat
        Start-Sleep -Seconds 2
        
        Test-Summarize
    }
    
    Write-Host "`n" + ("="*70) -ForegroundColor Cyan
    Write-Host "TEST SUITE COMPLETED".PadRight(70).Substring(0, 70) -ForegroundColor Cyan
    Write-Host ("="*70) -ForegroundColor Cyan
}

# ============================================================================
# USAGE
# ============================================================================

<#
To run tests, use one of these commands:

Run all tests:
    Run-AllTests

Run specific test:
    Test-HealthCheck
    Test-UserRegistration
    Test-UserLogin
    Test-DocumentUpload
    Test-GetDocument
    Test-ListDocuments
    Test-Search -Query "your search term"
    Test-Chat -Message "your question"
    Test-Summarize

Example workflow:
    Test-HealthCheck
    Test-UserLogin
    Test-DocumentUpload
    Test-GetDocument
    Test-Chat -Message "What is in this document?"
#>

# Auto-run all tests if script is executed directly
if ($MyInvocation.Line -like "*.ps1*") {
    Run-AllTests
}
