#!/usr/bin/env python3
"""
Quick diagnostic script to check OpenAI connection status.
Run this to see if your API key is working or if you're in mock mode.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("🔍 Prompt2Deck - OpenAI Connection Diagnostic")
print("=" * 60)

# Check 1: Is API key set?
api_key = os.getenv("OPENAI_API_KEY")
print("\n1️⃣ Checking API Key Configuration...")
if api_key:
    print(f"   ✅ API key is set (starts with: {api_key[:20]}...)")
else:
    print("   ⚠️  API key is NOT set")
    print("   → System will run in MOCK MODE (free, placeholder content)")
    sys.exit(0)

# Check 2: Test OpenAI connection
print("\n2️⃣ Testing OpenAI API Connection...")
try:
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    
    print("   Sending test request to OpenAI...")
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role": "user", "content": "Say: API working"}],
        max_tokens=10
    )
    
    print(f"   ✅ OpenAI API is WORKING!")
    print(f"   Response: {response.choices[0].message.content}")
    print(f"\n   Model: {response.model}")
    print(f"   Tokens used: {response.usage.total_tokens}")
    
except Exception as e:
    error_str = str(e)
    print(f"   ❌ OpenAI API connection FAILED")
    print(f"   Error: {error_str}")
    
    # Provide specific guidance based on error
    if "429" in error_str or "quota" in error_str.lower():
        print("\n" + "=" * 60)
        print("🚨 QUOTA EXCEEDED - Your API key is out of credits")
        print("=" * 60)
        print("\n📋 Solutions:")
        print("   1. Add credits at: https://platform.openai.com/account/billing")
        print("   2. Use mock mode: Comment out OPENAI_API_KEY in .env")
        print("   3. Get new API key: https://platform.openai.com/api-keys")
        print("\n💡 Mock mode works fine for testing!")
        
    elif "401" in error_str or "invalid" in error_str.lower():
        print("\n" + "=" * 60)
        print("🚨 INVALID API KEY")
        print("=" * 60)
        print("\n📋 Solutions:")
        print("   1. Get new API key: https://platform.openai.com/api-keys")
        print("   2. Check for typos in .env file")
        print("   3. Make sure key starts with 'sk-'")
        
    else:
        print("\n" + "=" * 60)
        print("🚨 CONNECTION ERROR")
        print("=" * 60)
        print("\n📋 Solutions:")
        print("   1. Check internet connection")
        print("   2. Try again in a few minutes")
        print("   3. Use mock mode for now")
    
    print("\n" + "=" * 60)
    sys.exit(1)

# Check 3: Test content generation
print("\n3️⃣ Testing Content Generation...")
try:
    test_response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": "You are a presentation expert."},
            {"role": "user", "content": "Generate 3 bullet points about AI. One per line."}
        ],
        max_tokens=100
    )
    
    print("   ✅ Content generation working!")
    print("   Sample output:")
    for line in test_response.choices[0].message.content.strip().split('\n')[:3]:
        print(f"      • {line.strip('- •')}")
    
except Exception as e:
    print(f"   ⚠️  Content generation issue: {str(e)}")

# Summary
print("\n" + "=" * 60)
print("📊 SUMMARY")
print("=" * 60)
print("\n✅ Your Prompt2Deck is ready to use with AI-powered content!")
print("\n💰 Cost per presentation: ~$0.01-0.05 (very cheap)")
print("📊 Check usage: https://platform.openai.com/usage")
print("\n🚀 Start the server: python main.py")
print("🌐 Open frontend: http://localhost:3000")
print("\n" + "=" * 60)
