@echo off
REM AcademiaPro Startup Script for Windows

echo ========================================
echo  AcademiaPro Server Setup & Launch
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Creating .env from .env.example...
    copy .env.example .env
    echo Please update .env with your actual API keys!
    pause
)

REM Check if venv exists
if not exist "venv" (
    echo.
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created.
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo.
echo Installing dependencies...
pip install -q --upgrade pip
pip install -q -r requirements.txt

REM Display startup info
echo.
echo ========================================
echo  Starting AcademiaPro Server
echo ========================================
echo.
echo Development Mode: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run Flask app
python app.py

pause
