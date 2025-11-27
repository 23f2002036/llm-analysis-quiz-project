"""Quick test to verify the setup is working correctly."""

import os
from dotenv import load_dotenv
import requests

load_dotenv()

def test_env_variables():
    """Test that all required environment variables are set."""
    print("🔍 Checking environment variables...")
    
    email = os.getenv("EMAIL")
    secret = os.getenv("SECRET")
    api_key = os.getenv("GOOGLE_API_KEY")
    
    checks = {
        "EMAIL": email,
        "SECRET": secret,
        "GOOGLE_API_KEY": api_key
    }
    
    all_good = True
    for key, value in checks.items():
        if value:
            masked_value = value[:10] + "..." if len(value) > 10 else value
            print(f"  ✅ {key}: {masked_value}")
        else:
            print(f"  ❌ {key}: NOT SET")
            all_good = False
    
    return all_good

def test_imports():
    """Test that all required packages are installed."""
    print("\n📦 Checking package imports...")
    
    packages = [
        ("playwright", "Playwright"),
        ("bs4", "BeautifulSoup"),
        ("langgraph", "LangGraph"),
        ("langchain", "LangChain"),
        ("langchain_google_genai", "Google GenAI"),
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
    ]
    
    all_good = True
    for module_name, display_name in packages:
        try:
            __import__(module_name.split(".")[0])
            print(f"  ✅ {display_name}")
        except ImportError:
            print(f"  ❌ {display_name}: NOT INSTALLED")
            all_good = False
    
    return all_good

def test_google_api():
    """Test Google API key validity."""
    print("\n🤖 Testing Google API key...")
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        # Simple test call
        response = llm.invoke("Say 'API key is valid!' if you can read this.")
        print(f"  ✅ API key is valid!")
        print(f"  Response: {response.content[:50]}...")
        return True
    except Exception as e:
        print(f"  ❌ API key test failed: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("🚀 LLM Analysis TDS Project 2 - Setup Verification")
    print("=" * 60)
    
    results = []
    
    results.append(("Environment Variables", test_env_variables()))
    results.append(("Package Imports", test_imports()))
    results.append(("Google API Key", test_google_api()))
    
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    all_passed = all(result[1] for result in results)
    
    for name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  {name}: {status}")
    
    print("=" * 60)
    
    if all_passed:
        print("\n✅ ALL TESTS PASSED! Your setup is ready.")
        print("\n📝 Next steps:")
        print("  1. Start the server: uv run main.py")
        print("  2. Test the endpoint in another terminal")
        print("  3. Deploy to HuggingFace Spaces or similar platform")
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
    
    return all_passed

if __name__ == "__main__":
    main()
