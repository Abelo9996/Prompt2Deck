# Frontend User Guide

## How the Frontend Works

The Prompt2Deck frontend is a simple, intuitive web interface with three main sections:

---

## 1. Input Section (Left Panel)

### What It Contains:
- **Text Area**: Large input box for your content
- **Preview Button**: Triggers AI to structure your slides
- **Helper Tips**: Guidance on input formats

### How to Use:

**Step 1: Enter Your Content**

You can enter content in three ways:

**Option A - Simple Topic:**
```
Explain Large Language Models
```
The AI will auto-generate a complete structure.

**Option B - Bullet List:**
```
Introduction to Machine Learning
* What is Machine Learning?
* Types of ML
* Applications
* Getting Started
```
Each bullet becomes a slide.

**Option C - Nested Outline:**
```
Cloud Computing Basics

1. Introduction
   - What is cloud computing?
   - Brief history

2. Service Models
   - IaaS
   - PaaS
   - SaaS

3. Benefits
   - Scalability
   - Cost efficiency
```
Full control over structure.

**Step 2: Click "Preview Slides"**
- The button sends your text to the backend
- AI processes it and returns structured slides
- Preview appears in the right panel
- Takes 5-15 seconds depending on complexity

---

## 2. Preview Section (Right Panel)

### What It Shows:

**Before Preview:**
- Empty state with document icon
- Text: "Preview will appear here"

**After Preview:**
- Total number of slides
- Each slide displayed as a card with:
  - **Slide number and title**
  - **Bullet points** (AI-expanded content)
  - **Speaker notes** (collapsible, at bottom)

### Example Preview:

```
5 slides total

┌─────────────────────────────────────┐
│ 1. Introduction to Machine Learning │
│ • Core concepts of automated learning│
│ • Why ML matters in today's world   │
│ • Basic terminology overview        │
│ Notes: When presenting this slide... │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ 2. Types of Machine Learning        │
│ • Supervised learning explained     │
│ • Unsupervised learning approaches  │
│ • Reinforcement learning basics     │
│ Notes: Emphasize the differences... │
└─────────────────────────────────────┘
```

### What You Can Do:
- **Review** the slide structure
- **Check** if content makes sense
- **Iterate** by editing input and re-previewing
- **Scroll** through all slides

---

## 3. Generate Section (Bottom Panel)

### What It Contains:
- **Configuration Options**:
  - ☑️ Include speaker notes
  - ☐ Generate images (requires DALL-E)
  - ☐ Export to PDF
  - Theme selector (Professional/Modern/Minimal)
- **Generate Deck Button**: Creates the final PPTX file

### How to Use:

**Step 1: Configure Options**

```
☑ Include speaker notes      ← Recommended for presenters
☐ Generate images            ← Costs money (DALL-E API)
☐ Export to PDF              ← Requires LibreOffice
Theme: Professional          ← Choose your style
```

**Step 2: Click "Generate Deck"**
- Shows progress spinner
- Takes 10-30 seconds
- Creates PPTX file on backend

**Step 3: Download**
- File automatically downloads
- Named: `presentation_YYYYMMDD_HHMMSS.pptx`
- Ready to present!

---

## Complete Workflow Example

### Scenario: Creating a Tech Presentation

**1. Start with Input:**
```
AI in Healthcare

* Medical Diagnosis
* Drug Discovery
* Patient Care
* Future Prospects
```

**2. Click "Preview Slides"**
- Wait 10 seconds
- See 5 slides appear:
  - Title slide
  - 4 content slides with expanded bullets

**3. Review Preview:**
```
Slide 1: AI in Healthcare
  • Overview and key topics
  • Healthcare transformation
  
Slide 2: Medical Diagnosis
  • AI-powered diagnostic tools
  • Improved accuracy rates
  • Real-world applications
  
[etc...]
```

**4. Configure Options:**
- ☑ Speaker notes: Yes
- ☐ Images: No (save API costs)
- ☐ PDF: No
- Theme: Professional

**5. Click "Generate Deck"**
- Wait 15 seconds
- Download `presentation_20251207_143052.pptx`

**6. Open in PowerPoint:**
- 5 professionally formatted slides
- Clean blue theme
- Speaker notes included
- Ready to present!

---

## Tips for Best Results

### Input Tips:
1. **Be Specific**: "Explain ML for beginners" is better than just "ML"
2. **Use Structure**: Organized outlines produce better slides
3. **Keep it Focused**: 5-10 slides is ideal
4. **Iterate**: Preview, refine input, preview again

### Preview Tips:
1. **Check Titles**: Are they clear and descriptive?
2. **Review Bullets**: Do they make sense together?
3. **Read Notes**: Are speaker notes helpful?
4. **Verify Count**: Too many/few slides?

### Generation Tips:
1. **Speaker Notes**: Always useful, no extra cost
2. **Images**: Skip unless you need them (costs money)
3. **PDF**: Only if you need it (requires setup)
4. **Theme**: Professional is safe for most cases

---

## What's NOT Finished Yet

### ✅ Fully Implemented:
- Input text area
- Preview functionality
- Slide structure generation
- Content expansion via AI
- Speaker notes generation
- PPTX file creation
- Theme support
- File download

### ⚠️ Partially Implemented:
- **Image Generation**: Code is there but requires:
  - `USE_DALLE=true` in backend/.env
  - Additional API costs
  - Images currently use placeholders

- **PDF Export**: Code is there but requires:
  - LibreOffice installed on system
  - System command access
  - May not work on all systems

### 🔧 Could Be Added (Future):
- **Real-time preview** (without clicking button)
- **Slide reordering** (drag and drop)
- **Custom templates** (upload your own)
- **Slide editing** (modify individual slides)
- **History** (save previous generations)
- **User accounts** (save preferences)
- **Collaboration** (share with team)
- **More export formats** (Google Slides, Keynote)

---

## Common Issues & Solutions

### Issue: Preview Button Does Nothing
**Solution**: 
- Check backend is running: `curl http://localhost:8000/`
- Check browser console (F12) for errors
- Verify text area is not empty

### Issue: Preview Takes Forever
**Solution**:
- Check OpenAI API key is valid
- System works in "mock mode" if no key (faster but less smart)
- Check internet connection

### Issue: Download Doesn't Start
**Solution**:
- Check browser popup blocker
- Check backend output directory exists
- Verify file was created in `backend/output/`

### Issue: Generated Slides Look Wrong
**Solution**:
- Try different theme
- Regenerate with different options
- Edit input text and try again

---

## Advanced Usage

### Using Without Frontend

You can skip the frontend entirely and use the API:

```bash
# Direct API call
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "Your content here",
    "include_speaker_notes": true,
    "generate_images": false,
    "theme": "professional"
  }'
```

### Programmatic Usage

```python
import requests

response = requests.post("http://localhost:8000/generate", json={
    "input_text": "Introduction to Python",
    "include_speaker_notes": True,
    "generate_images": False,
    "theme": "modern"
})

print(f"File: {response.json()['file_path']}")
```

---

## Summary: What's Complete vs Incomplete

### ✅ 100% Complete & Working:
1. Text input with format detection
2. AI-powered slide structuring
3. Content expansion with LLM
4. Speaker notes generation
5. Preview display with all details
6. PPTX file generation
7. Theme support (3 themes)
8. File download
9. Error handling
10. Mock mode (no API key needed)

### ⚠️ 90% Complete (Works but needs setup):
1. Image generation (needs USE_DALLE=true + costs)
2. PDF export (needs LibreOffice installed)

### 📋 Not Started (Future Features):
1. Real-time collaboration
2. User authentication
3. Slide templates
4. Custom fonts/colors
5. Animation effects
6. Presentation history
7. Cloud storage integration

---

## The Bottom Line

**The frontend is fully functional for core features:**
- Enter text → Preview slides → Generate deck → Download

**Everything works out of the box except:**
- DALL-E images (optional, needs API key + costs)
- PDF export (optional, needs LibreOffice)

**You can use it right now to:**
- Create professional presentations
- Expand outlines into full decks
- Generate speaker notes
- Choose themes
- Download PPTX files

**It's production-ready for the core use case!** 🎯
