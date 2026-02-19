from .llm_client import llm_client

class ChatService:
    def get_response(self, message: str, context: str = "") -> dict:
        """
        Generates a helpful response for the chatbot.
        """
        system_instruction = """
        You are 'MarketMind AI', a helpful and intelligent assistant for a Revenue Intelligence Platform.
        Your goal is to help users with marketing strategies, competitor analysis, and navigating the platform.
        
        Keep your answers concise, professional, and friendly.
        If the user asks about the platform's features, explain them:
        - Competitor Intelligence: Analyzes competitor websites.
        - Revenue Simulator: Projects future revenue based on metrics.
        - Campaign Generator: Creates ad copy and strategies.
        
        If the user asks specifically about "Revenue Growth" or charts, explain that the dashboard visualizes their simulated data.
        """
        
        prompt = f"User Message: {message}\n\nContext (if any): {context}"
        
        try:
            response_text = llm_client.generate(prompt, system_instruction)
            return {"response": response_text}
        except Exception as e:
            return {"error": f"Chat failed: {str(e)}"}

chat_service = ChatService()
