from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('AIPIPE_TOKEN')

# Try with OpenAI client directly
client = OpenAI(
    api_key=token,
    base_url="https://aiproxy.sanand.workers.dev/openai/v1"
)

print("Testing with OpenAI client...")
print(f"Token: {token[:30]}...")
print()

try:
    # Try to make a simple completion
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Say 'Hello'"}],
        max_tokens=10
    )
    print("✅ SUCCESS!")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ Error: {str(e)[:500]}")
