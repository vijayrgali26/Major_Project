param(
    [int]$Port = 5000,
    [string]$Config = 'development'
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

Write-Host "Building frontend..."
npm --prefix .\frontend run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "Frontend build failed with exit code $LASTEXITCODE" -ForegroundColor Red
    exit $LASTEXITCODE
}

if ($Config -eq 'production' -and -not $env:DATABASE_URL) {
    Write-Host "WARNING: DATABASE_URL is not set, falling back to development configuration." -ForegroundColor Yellow
    $Config = 'development'
}

Write-Host "Starting backend on port $Port using config '$Config'..."
$env:FLASK_CONFIG = $Config
$env:PORT = $Port.ToString()
python .\backend\run.py
