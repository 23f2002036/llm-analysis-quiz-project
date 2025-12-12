#!/usr/bin/env python3
"""
Test script to interact with the TDS LLM Analysis project.
Usage:
  1. Start by visiting: https://tds-llm-analysis.s-anand.net/project2
  2. Read the task instructions on the page.
  3. Run this script to submit answers.
"""

import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

# Configuration
TDS_SERVER = "https://tds-llm-analysis.s-anand.net"
EMAIL = os.getenv("EMAIL")
SECRET = os.getenv("SECRET")

def submit_answer(url: str, answer: str) -> dict:
    """Submit an answer to the TDS server."""
    if not EMAIL or not SECRET:
        raise ValueError("EMAIL and SECRET must be set in .env file")
    
    payload = {
        "email": EMAIL,
        "secret": SECRET,
        "url": url,
        "answer": answer
    }
    
    print(f"\n📤 Submitting to {TDS_SERVER}/submit")
    print(f"   Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            f"{TDS_SERVER}/submit",
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        print(f"\n✅ Response: {json.dumps(result, indent=2)}")
        return result
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error: {e}")
        return None

def main():
    print("=" * 60)
    print("TDS LLM Analysis - Test Submission Script")
    print("=" * 60)
    print(f"\n📧 Email: {EMAIL}")
    print(f"🔑 Secret: {'***' if SECRET else 'NOT SET'}")
    
    if not EMAIL or not SECRET:
        print("\n❌ ERROR: EMAIL and SECRET not set in .env file")
        return
    
    # Step 1: Start with the project2 URL
    print(f"\n📍 Step 1: Visit {TDS_SERVER}/project2 in your browser")
    print("   Read the task instructions carefully.")
    
    # Step 2: Get the answer from user
    url = input("\n🔗 Enter the URL from the task page (e.g., https://tds-llm-analysis.s-anand.net/project2): ").strip()
    answer = input("💬 Enter your answer: ").strip()
    
    if not url or not answer:
        print("❌ URL and answer are required")
        return
    
    # Step 3: Submit
    result = submit_answer(url, answer)
    
    if result:
        if result.get("correct"):
            print("\n🎉 Correct! Next URL:", result.get("next_url", "No next URL"))
        else:
            print("\n❌ Incorrect. Try again.")
        
        # If there's a next URL, suggest opening it
        if result.get("next_url"):
            print(f"\n📖 Open this in your browser: {result['next_url']}")

if __name__ == "__main__":
    main()
