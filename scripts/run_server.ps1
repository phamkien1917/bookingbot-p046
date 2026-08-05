$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
Push-Location $root

$pythonExe = "python"
$venvPython = Join-Path $root ".venv\Scripts\python.exe"
if (Test-Path $venvPython) {
    $pythonExe = $venvPython
}

Write-Host "Starting BookingBot server from $root" -ForegroundColor Cyan

& $pythonExe -c "import fastapi, uvicorn" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    & $pythonExe -m pip install -r requirements.txt
}

& $pythonExe -m uvicorn src.main:app --reload --host 127.0.0.1 --port 8000

Pop-Location
