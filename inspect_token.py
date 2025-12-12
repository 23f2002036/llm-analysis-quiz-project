import os
import json
import base64
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('AIPIPE_TOKEN')
print(f"Full token: {token}")
print(f"Token length: {len(token)}")
print(f"Token has spaces: {' ' in token}")
print(f"Token has newlines: {'\\n' in token or '\\r' in token}")
print()

# Try to decode the JWT to see what's inside
try:
    parts = token.split('.')
    print(f"JWT has {len(parts)} parts (should be 3)")
    print()
    
    if len(parts) == 3:
        # Decode header
        header_padding = parts[0] + '=' * (4 - len(parts[0]) % 4)
        header = json.loads(base64.urlsafe_b64decode(header_padding))
        print(f"Header: {json.dumps(header, indent=2)}")
        print()
        
        # Decode payload
        payload_padding = parts[1] + '=' * (4 - len(parts[1]) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_padding))
        print(f"Payload: {json.dumps(payload, indent=2)}")
        print()
        
        print(f"Signature (last 20 chars): ...{parts[2][-20:]}")
except Exception as e:
    print(f"Error decoding JWT: {e}")
