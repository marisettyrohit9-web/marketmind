import os
import json
from google import genai
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        
        # Initialize clients
        self.gemini_client = None
        if self.gemini_api_key:
            try:
                self.gemini_client = genai.Client(api_key=self.gemini_api_key)
            except:
                pass
                
        self.groq_client = None
        if self.groq_api_key:
            self.groq_client = Groq(api_key=self.groq_api_key)

    def _generate_with_gemini(self, prompt, system_instruction=None):
        if not self.gemini_client:
            raise ValueError("Gemini client not initialized")
            
        # Try multiple model names if one fails
        # Updated list with more recent model versions
        models_to_try = [
            "gemini-2.0-flash", 
            "gemini-1.5-flash", 
            "gemini-1.5-pro",
            "gemini-1.0-pro"
        ]
        last_error = None
        
        for model in models_to_try:
            try:
                response = self.gemini_client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=genai.types.GenerateContentConfig(
                        system_instruction=system_instruction
                    ) if system_instruction else None
                )
                return response.text
            except Exception as e:
                # print(f"DEBUG: Failed with model {model}: {e}") # Optional debug print
                last_error = e
                continue
        raise last_error

    def _generate_with_groq(self, prompt, system_instruction=None):
        if not self.groq_client:
            raise ValueError("Groq client not initialized")
            
        full_prompt = f"{system_instruction}\n\n{prompt}" if system_instruction else prompt
        chat_completion = self.groq_client.chat.completions.create(
            messages=[
                {"role": "user", "content": full_prompt}
            ],
            # Updated to a currently supported model
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content

    def generate(self, prompt: str, system_instruction: str = None) -> str:
        # Try Gemini First
        if self.gemini_client:
            try:
                return self._generate_with_gemini(prompt, system_instruction)
            except Exception as e:
                print(f"Gemini failed: {e}. Falling back to Groq...")
        
        # Fallback to Groq
        if self.groq_client:
            try:
                return self._generate_with_groq(prompt, system_instruction)
            except Exception as e:
                return f"Error with Groq: {e}"
                
        return "Error: No working API providers found."
    
    def generate_json(self, prompt: str, schema: dict = None) -> dict:
        """
        Generates structured JSON output.
        """
        system_instruction = "You are a data extraction assistant. Output valid JSON only."
        if schema:
            system_instruction += f" Follow this schema: {json.dumps(schema)}"
        
        raw_response = self.generate(prompt + "\n\nReturn strictly valid JSON.", system_instruction)
        
        # Robust JSON extraction using regex
        try:
            # Find the first '{' and the last '}'
            start_index = raw_response.find('{')
            end_index = raw_response.rfind('}')
            
            if start_index != -1 and end_index != -1:
                cleaned_response = raw_response[start_index:end_index+1]
                return json.loads(cleaned_response)
            else:
                 # Fallback: try cleaning markdown blocks if regex fails (though regex should catch it)
                 cleaned_response = raw_response.replace("```json", "").replace("```", "").strip()
                 return json.loads(cleaned_response)
                 
        except json.JSONDecodeError:
            # Fallback or error handling
            print(f"Failed to decode JSON. Raw response: {raw_response}")
            return {"error": "Failed to generate valid JSON", "raw": raw_response}

llm_client = LLMClient()
