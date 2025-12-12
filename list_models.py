"""List available OpenAI models via AI Pipe."""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("AIPIPE_TOKEN"),
    base_url="https://aipipe.org/openai/v1"
)

print("Available OpenAI models via AI Pipe:")
print("=" * 60)
try:
    models = client.models.list()
    for model in models.data:
        print(f" {model.id}")
        print()
except Exception as e:
    print(f"Error: {e}")
