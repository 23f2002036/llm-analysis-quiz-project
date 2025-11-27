"""List available Gemini models."""
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

print("Available Gemini models:")
print("=" * 60)
try:
    for model in client.models.list():
        print(f"✅ {model.name}")
        print(f"   Display: {model.display_name}")
        print()
except Exception as e:
    print(f"Error: {e}")
