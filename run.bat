@echo off
setlocal

if not exist venv (
    echo Virtual environment not found. Running setup...
    call setup.bat
)

call venv\Scripts\activate
echo Starting Backend Server...
venv\Scripts\python -m uvicorn main:app --reload
