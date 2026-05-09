@echo off
REM Quiz Management System - Setup and Run Script for Windows

echo.
echo =============================================
echo Quiz Management System - Setup Script
echo =============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please download Python from: https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Checking dependencies...
python --version

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo.
    echo [2/5] Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
) else (
    echo.
    echo [2/5] Virtual environment already exists, skipping creation...
)

echo.
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [4/5] Installing dependencies...
pip install -r requirements.txt

echo.
echo [5/5] Setup complete!
echo.
echo =============================================
echo Starting Quiz Management System...
echo =============================================
echo.
echo Application will run at: http://localhost:5000
echo.
echo Make sure:
echo - XAMPP MySQL server is running
echo - Database 'quiz_system' is created with tables
echo - MySQL credentials in config.py are correct
echo.

python run.py

pause
