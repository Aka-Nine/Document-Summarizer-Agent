<#
PowerShell helper to set common repository secrets using the GitHub CLI (`gh`).

Usage:
  1. Install GitHub CLI and authenticate: `gh auth login`
  2. Run this script (it will prompt for values if not passed):
     `pwsh .\scripts\set_github_secrets.ps1`

This script does NOT store any secrets in the repo. It uses `gh secret set` to put secrets in the repository.
#>

Param(
    [string]$Repo = "",
    [switch]$Interactive
)

function Set-SecretIfProvided {
    param($name, $value)
    if (-not $value) {
        if ($Interactive) {
            $value = Read-Host -AsSecureString "Enter value for $name"
            $bstr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($value)
            $plain = [System.Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
            [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
        } else {
            return
        }
    }
    gh secret set $name --body $plain --repo $Repo
    Write-Host "Set secret $name"
}

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Error "GitHub CLI 'gh' not found. Install from https://cli.github.com/ and run 'gh auth login' first."
    exit 1
}

if (-not $Repo) {
    $Repo = gh repo view --json nameWithOwner -q .nameWithOwner
}

Write-Host "Using repository: $Repo"

# Common secrets to set (match names used in CI/workflow)
$secrets = @(
    "SECRET_KEY",
    "MONGODB_URL",
    "MONGODB_DB_NAME",
    "REDIS_CLOUD_PASSWORD",
    "CHROMA_API_KEY",
    "CHROMA_TENANT",
    "CHROMA_DATABASE",
    "GEMINI_API_KEY",
    "OPENAI_API_KEY",
    "GROQ_API_KEY"
)

foreach ($s in $secrets) {
    if ($Interactive) {
        $val = Read-Host -AsSecureString "Enter value for $s (leave blank to skip)"
        if ($val.Length -gt 0) {
            $bstr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($val)
            $plain = [System.Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
            [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
            gh secret set $s --body $plain --repo $Repo
            Write-Host "Set secret $s"
        }
    } else {
        Write-Host "Interactive mode not enabled. To set $s run: gh secret set $s --body <value> --repo $Repo"
    }
}

Write-Host "Secrets helper finished. Ensure required secrets are set in the repository settings."
