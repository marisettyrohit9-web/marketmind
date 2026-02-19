from .llm_client import llm_client

class CampaignService:
    def generate_campaign(self, data: dict):
        audience = data.get("audience", "General Audience")
        revenue_goal = data.get("revenue_goal", "Maximize Revenue")
        competitor_insight = data.get("competitor_insight", "")

        prompt = f"""
        Generate a high-converting digital marketing campaign strategy based on the following inputs:
        
        Target Audience: {audience}
        Revenue Goal: {revenue_goal}
        Competitor Insight (if any): {competitor_insight}
        
        Generate the following components:
        1. 3 Ad Copy Variations (Headline + Body text)
        2. 2 Unique Value Propositions (UVPs)
        3. 1 Emotional Hook
        4. 1 Call to Action (CTA)
        5. Recommended Marketing Platform (e.g., LinkedIn, Facebook, Google Ads) with reasoning.
        
        Return ONLY valid JSON with keys:
        ad_copies (list of objects with headline, body), value_propositions (list), emotional_hook, cta, recommended_platform, reasoning.
        """
        
        try:
            schema = {
                "ad_copies": [{"headline": "string", "body": "string"}],
                "value_propositions": ["string"],
                "emotional_hook": "string",
                "cta": "string",
                "recommended_platform": "string",
                "reasoning": "string"
            }
            
            return llm_client.generate_json(prompt, schema)
        except Exception as e:
            return {"error": f"Campaign generation failed: {str(e)}"}

campaign_service = CampaignService()
