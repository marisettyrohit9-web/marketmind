# MarketMind AI - Revenue Intelligence Platform

High-performance SaaS dashboard for revenue simulation and competitor intelligence.

## Tech Stack
- **Frontend**: React, Vite, Tailwind CSS (v3), Chart.js
- **Backend**: FastAPI, Python, AI (Groq/Gemini)

## Quick Start

1. **Setup Backend**:
   - Double-click `setup_backend.bat` to automatically set up Python and dependencies.
   - **Important**: Create a `.env` file in the `backend` folder (copy `.env.example`) and add your API keys.

2. **Run Application**:
   - Double-click `start_app.bat`.
   - Frontend: http://localhost:5173
   - Backend: http://localhost:8000

## Troubleshooting

### "Python not found"
If `setup_backend.bat` fails, install Python from [python.org](https://www.python.org/downloads/) and ensure **"Add Python to PATH"** is checked during installation.

### Frontend Errors
If the frontend shows a blank screen or errors:
```bash
cd frontend
npm install
npm run dev
```
