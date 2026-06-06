@echo off
setlocal enabledelayedexpansion

set PORT=%1
if "%PORT%"=="" set PORT=5000
set CONFIG=%2
if "%CONFIG%"=="" set CONFIG=development

cd /d "%~dp0"

echo Building frontend...
npm --prefix frontend run build
if errorlevel 1 (
  echo Frontend build failed.
  exit /b 1
)

echo Starting backend on port %PORT% using config %CONFIG%...
if "%CONFIG%"=="production" if not defined DATABASE_URL (
  echo WARNING: DATABASE_URL is not set, falling back to development configuration.
  set CONFIG=development
)
set FLASK_CONFIG=%CONFIG%
set PORT=%PORT%
python backend\run.py
