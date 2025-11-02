@echo off
REM Quick Start Script for Universal Web Scraper & Downloader (Windows)

echo ================================================================
echo    Universal Web Scraper ^& Downloader - Quick Start
echo ================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed. Please install Python 3 first.
    pause
    exit /b 1
)

echo √ Python found
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo X Failed to install dependencies
    pause
    exit /b 1
)

echo √ Dependencies installed successfully
echo.

REM Ask user which mode to run
echo Choose how to run the app:
echo 1. Web Interface (recommended)
echo 2. Command Line Interface
echo.
set /p choice="Enter choice (1 or 2): "

if "%choice%"=="1" (
    echo.
    echo Starting web interface...
    echo Open your browser to: http://localhost:5000
    echo.
    python app.py
) else if "%choice%"=="2" (
    echo.
    echo Starting command line interface...
    echo.
    python main.py
) else (
    echo Invalid choice. Exiting.
    pause
    exit /b 1
)

pause
