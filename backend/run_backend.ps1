$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $scriptDir 'venv\Scripts\python.exe'

if (-not (Test-Path $python)) {
    Write-Host 'Virtual environment not found. Create it first with: python -m venv venv' -ForegroundColor Yellow
    exit 1
}

Set-Location $scriptDir
& $python -m uvicorn main:app --reload
