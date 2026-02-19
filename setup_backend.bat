@echo off
setlocal

echo ==========================================
echo MarketMind AI - Backend Setup
echo ==========================================

REM Check if Python is actually working (filters out the Windows Store shim)
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    goto :PYTHON_FOUND
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    goto :PYTHON_FOUND
)

echo.
echo [ERROR] Python is not installed or not in your PATH.
echo.
echo Attempting to install Python 3.11 via Winget...
winget install -e --id Python.Python.3.11
if %errorlevel% neq 0 (
    echo.
    echo [FATAL] Winget installation failed.
    echo Please manually install Python from: https://www.python.org/downloads/
    echo IMPORTANT: Check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo.
echo Python installed successfully! You may need to restart this script.
echo Press any key to try continuing...
pause
set PYTHON_CMD=python

:PYTHON_FOUND
echo Found working Python: %PYTHON_CMD%

cd backend
if not exist venv (
    echo Creating virtual environment...
    %PYTHON_CMD% -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ==========================================
echo Setup Complete!
echo You can now run 'start_app.bat'
echo ==========================================
pause
