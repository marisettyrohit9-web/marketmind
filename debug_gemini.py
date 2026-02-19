import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not found in .env")
    exit(1)

print(f"Using API Key: {api_key[:5]}...{api_key[-4:]}")

client = genai.Client(api_key=api_key)

print("\n--- Listing Models ---")
try:
    for m in client.models.list():
        print(f"Found: {m.name}")
except Exception as e:
    print(f"List failed: {e}")

print("\n--- Testing Generation ---")
test_models = [
    "gemini-1.5-flash",
    "models/gemini-1.5-flash",
    "gemini-1.5-pro",
    "models/gemini-1.5-pro",
    "gemini-pro",
    "models/gemini-pro"
]

for model_name in test_models:
    print(f"\nTesting: {model_name}")
    try:
        response = client.models.generate_content(
            model=model_name,
            contents='Hello'
        )
        print(f"SUCCESS! Model '{model_name}' works.")
        break
    except Exception as e:
        print(f"Failed: {str(e)[:100]}...")
