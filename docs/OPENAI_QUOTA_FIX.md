# OpenAI API Quota Issue - Troubleshooting Guide

## Problem Identified

Your OpenAI API key has **exceeded its quota**. This is why the connection isn't working.

## Error Message
```
Error code: 429 - insufficient_quota
You exceeded your current quota, please check your plan and billing details.
```

---

## Solutions

### Option 1: Add Credits to Your OpenAI Account (Recommended)

1. **Go to OpenAI Platform**: https://platform.openai.com/
2. **Navigate to Billing**: https://platform.openai.com/account/billing/overview
3. **Add Payment Method**: Add a credit card if not already added
4. **Add Credits**: Purchase additional credits ($5-$20 recommended)
5. **Wait 1-2 minutes** for credits to activate
6. **Restart the backend** and test again

### Option 2: Get a New API Key

1. **Go to API Keys**: https://platform.openai.com/api-keys
2. **Create New Key**: Click "Create new secret key"
3. **Copy the Key**: Save it immediately (you can't see it again)
4. **Update .env**:
   ```bash
   cd backend
   nano .env  # or use any text editor
   # Replace OPENAI_API_KEY with your new key
   ```
5. **Restart the backend**

### Option 3: Use Mock Mode (No API Key Needed)

The system has a built-in **mock mode** that works without OpenAI:

1. **Remove or comment out the API key** in `backend/.env`:
   ```bash
   # OPENAI_API_KEY=your_key_here
   ```

2. **Restart the backend**:
   ```bash
   cd backend
   source venv/bin/activate
   python main.py
   ```

3. **What happens in mock mode:**
   - ✅ System still works
   - ✅ Generates slide structure
   - ✅ Creates PPTX files
   - ⚠️ Uses placeholder content (not AI-generated)
   - ⚠️ Generic bullet points
   - ⚠️ Generic speaker notes

**Mock mode output example:**
```
Title: "Machine Learning"
Bullets:
- Key insight about Machine Learning
- Important consideration for Machine Learning
- Practical application of Machine Learning
Notes: When presenting this slide, emphasize the key concepts...
```

---

## Quick Test After Fix

### Test 1: Verify API Key Works
```bash
cd backend
source venv/bin/activate
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[{'role': 'user', 'content': 'Say hello'}],
    max_tokens=10
)
print('✅ Success:', response.choices[0].message.content)
"
```

**Expected output:**
```
✅ Success: Hello! How can I assist you today?
```

### Test 2: Test the Pipeline
```bash
cd backend
python test_pipeline.py
```

**Should generate a test presentation without errors.**

### Test 3: Test via Frontend
1. Open http://localhost:3000
2. Enter: "Introduction to AI"
3. Click "Preview Slides"
4. Should see AI-generated content (not placeholder text)

---

## How to Check Your OpenAI Usage

1. **Go to**: https://platform.openai.com/usage
2. **Check**:
   - Current usage
   - Remaining credits
   - Billing status

---

## Cost Estimates (if adding credits)

**For Prompt2Deck usage:**
- Model: `gpt-4o-mini` (cheapest option)
- Cost: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
- Per presentation: ~$0.01-0.05 (very cheap!)
- $5 credit = ~100-500 presentations

**Recommendations:**
- Start with **$5** - plenty for testing
- Monitor usage at: https://platform.openai.com/usage
- Set spending limits in billing settings

---

## Why Mock Mode Exists

The system was designed to work **with or without** an API key:

**Without API key (Mock Mode):**
- ✅ Free to use
- ✅ Fast (no API calls)
- ✅ Good for testing structure
- ⚠️ Generic content

**With API key (AI Mode):**
- ✅ High-quality content
- ✅ Smart bullet expansion
- ✅ Professional speaker notes
- ⚠️ Costs money (very little)
- ⚠️ Slower (API calls)

---

## Fix Summary

### Immediate Solution (Free):
```bash
# Option 1: Use mock mode
cd backend
# Comment out OPENAI_API_KEY in .env
python main.py
```

### Best Solution (Small cost):
```bash
# Option 2: Add credits to OpenAI account
1. Add $5-20 to OpenAI account
2. Wait 1-2 minutes
3. Restart backend
```

---

## Code Fix Applied

I've already updated `main.py` to properly load environment variables:

```python
from dotenv import load_dotenv
load_dotenv()  # This ensures .env is loaded
```

Now the system will correctly read your API key from the `.env` file.

---

## Next Steps

**Choose one:**

1. **Continue with mock mode** (free, works now)
   - Comment out API key
   - Restart backend
   - Use with placeholder content

2. **Add credits** (best quality, small cost)
   - Add $5 to OpenAI account
   - Keep using same API key
   - Get AI-generated content

3. **Get new key** (if account has issues)
   - Create new OpenAI account
   - Get free trial credits
   - Update .env with new key

**The system works either way!** 🎯
