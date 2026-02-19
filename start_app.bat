@echo off
echo Starting MarketMind AI...

start cmd /k "cd backend && venv\Scripts\activate && uvicorn main:app --reload"
start cmd /k "cd frontend && npm run dev"

echo Backend running at http://localhost:8000
echo Frontend running at http://localhost:5173
