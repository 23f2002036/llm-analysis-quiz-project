"""
Test script for the LLM Analysis Quiz Solver API
"""
import requests
import json
import time

BASE_URL = "http://localhost:7860"

def test_healthz():
    """Test the healthz endpoint"""
    print("1. Testing /healthz endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/healthz", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_solve():
    """Test the /solve endpoint"""
    print("\n2. Testing /solve endpoint...")
    
    payload = {
        "url": "https://tds-llm-analysis.s-anand.net/demo",
        "secret": "monika@495"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/solve",
            json=payload,
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_wrong_secret():
    """Test with wrong secret"""
    print("\n3. Testing /solve with wrong secret...")
    
    payload = {
        "url": "https://tds-llm-analysis.s-anand.net/demo",
        "secret": "wrong_secret"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/solve",
            json=payload,
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        # Should be 403
        return response.status_code == 403
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Testing LLM Analysis Quiz Solver API")
    print("=" * 60)
    
    results = []
    
    # Give server a moment to fully start
    time.sleep(1)
    
    results.append(("Healthz", test_healthz()))
    results.append(("Solve Endpoint", test_solve()))
    results.append(("Wrong Secret", test_wrong_secret()))
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  {name}: {status}")
    
    if all(r[1] for r in results):
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed")
