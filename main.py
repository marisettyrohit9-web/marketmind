from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from dotenv import load_dotenv
import os

from services.competitor_service import competitor_service
from services.revenue_service import revenue_service
from services.campaign_service import campaign_service

load_dotenv()

app = FastAPI(title="MarketMind AI API", version="1.0.0")

# CORS Configuration
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "*" # Allow all for debugging
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models ---

class CompetitorRequest(BaseModel):
    url: str

class RevenueSimulationRequest(BaseModel):
    visitors: int
    conversion_rate: float
    average_order_value: float
    ad_spend: float

class CampaignRequest(BaseModel):
    audience: str
    revenue_goal: str
    competitor_insight: Optional[str] = ""

# --- Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Welcome to MarketMind AI API", "status": "active"}

@app.post("/api/competitor/analyze")
async def analyze_competitor(request: CompetitorRequest):
    result = competitor_service.analyze_competitor(request.url)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.post("/api/revenue/simulate")
async def simulate_revenue(request: RevenueSimulationRequest):
    result = revenue_service.simulate_revenue(request.dict())
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.post("/api/campaign/generate")
async def generate_campaign(request: CampaignRequest):
    result = campaign_service.generate_campaign(request.dict())
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

# --- Chat Endpoint ---
class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = ""

from services.chat_service import chat_service

@app.post("/api/chat/send")
async def send_chat(request: ChatRequest):
    result = chat_service.get_response(request.message, request.context)
    if "error" in result:
         # Log the error but return a friendly message if possible, or raise HTTP exception
         raise HTTPException(status_code=500, detail=result["error"])
    return result
