import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('AIPIPE_TOKEN')
print(f"Testing token: {token[:30]}...")
print()

# Different possible endpoints to try
endpoints = [
    "https://aiproxy.sanand.workers.dev/openai/v1/models",
    "https://aiproxy.sanand.workers.dev/v1/models",
    "https://api.aiproxy.sanand.workers.dev/openai/v1/models",
    "https://aiproxy.sanand.workers.dev/openai/models",
]

for i, endpoint in enumerate(endpoints, 1):
    print(f"{i}. Testing endpoint: {endpoint}")
    try:
        response = requests.get(
            endpoint,
            headers={'Authorization': f'Bearer {token}'},
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ SUCCESS!")
            print(f"   Response: {response.json()}")
        else:
            error_msg = response.text[:150]
            print(f"   ❌ Error: {error_msg}")
    except Exception as e:
        print(f"   ❌ Exception: {str(e)[:100]}")
    print()
