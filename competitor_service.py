import requests
from bs4 import BeautifulSoup
from .llm_client import llm_client

class CompetitorService:
    def analyze_competitor(self, url: str):
        try:
            # 1. Fetch content
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # 2. Extract text
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "header", "footer", "nav"]):
                script.decompose()
                
            text = soup.get_text(separator=' ', strip=True)
            
            # Limit text length to avoid token limits (approx 4000 chars)
            truncated_text = text[:4000]
            
            if not truncated_text:
                return {"error": "Could not extract meaningful text from the page."}

            # 3. Analyze with LLM
            prompt = f"""
            Analyze the following competitor website content and provide strategic insights.
            
            Website Content:
            {truncated_text}
            
            Focus on:
            1. Market Positioning: How do they describe themselves?
            2. Strengths: What are their key selling points?
            3. Weaknesses: What seems missing or weak?
            4. Market Gaps: Opportunities they aren't addressing.
            5. Recommended Strategy: How to compete against them.
            
            Return ONLY valid JSON with keys: 
            positioning, strengths (list), weaknesses (list), market_gaps (list), recommended_strategy, confidence_score (number 0-100).
            """
            
            schema = {
                "positioning": "string",
                "strengths": ["string"],
                "weaknesses": ["string"],
                "market_gaps": ["string"],
                "recommended_strategy": "string",
                "confidence_score": 0
            }
            
            result = llm_client.generate_json(prompt, schema)
            return result

        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch URL: {str(e)}"}
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}

competitor_service = CompetitorService()
