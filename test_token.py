import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('AIPIPE_TOKEN')
print(f"Token (first 30 chars): {token[:30]}...")
print(f"Token length: {len(token)}")
print()

# Test with Bearer prefix
print("1. Testing with 'Bearer' prefix:")
response = requests.get(
    'https://aiproxy.sanand.workers.dev/openai/v1/models',
    headers={'Authorization': f'Bearer {token}'}
)
print(f"   Status: {response.status_code}")
if response.status_code != 200:
    print(f"   Error: {response.text[:200]}")
else:
    print("   ✅ Success!")

print()

# Test without Bearer prefix
print("2. Testing without 'Bearer' prefix:")
response = requests.get(
    'https://aiproxy.sanand.workers.dev/openai/v1/models',
    headers={'Authorization': token}
)
print(f"   Status: {response.status_code}")
if response.status_code != 200:
    print(f"   Error: {response.text[:200]}")
else:
    print("   ✅ Success!")
