"""
Simple test to verify imports and basic functionality
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("Testing Imports")
print("=" * 60)

try:
    print("1. Testing FastAPI imports...")
    from fastapi import FastAPI
    print("   ✅ FastAPI imported")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

try:
    print("2. Testing LangChain imports...")
    from langchain.chat_models import init_chat_model
    print("   ✅ LangChain imported")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

try:
    print("3. Testing agent imports...")
    from agent import run_agent
    print("   ✅ Agent imported")
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("4. Testing tools imports...")
    from tools import get_rendered_html, download_file, post_request, run_code, add_dependencies
    print("   ✅ Tools imported")
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ All imports successful!")
print("=" * 60)
