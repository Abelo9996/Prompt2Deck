# System Flow Diagram

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          User Interaction                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Web Interface (Next.js)          API Clients (curl, Python, etc.)  │
│         │                                      │                     │
│         └──────────────────┬───────────────────┘                     │
│                            │                                         │
└────────────────────────────┼─────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      FastAPI Server (Port 8000)                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Endpoints:                                                          │
│  • GET  /           → Health Check                                   │
│  • POST /preview    → Generate Structure Preview                     │
│  • POST /generate   → Create Complete Deck                           │
│  • GET  /download   → Download Generated File                        │
│                                                                       │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        Processing Pipeline                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│   ┌────────────────┐      ┌────────────────┐      ┌──────────────┐ │
│   │ Outline Parser │  →   │    Content     │  →   │    Image     │ │
│   │                │      │   Generator    │      │  Generator   │ │
│   └────────────────┘      └────────────────┘      └──────────────┘ │
│          │                        │                       │         │
│          │                        ▼                       │         │
│          │                 ┌─────────────┐               │         │
│          │                 │  OpenAI API │               │         │
│          │                 │ (GPT Model) │               │         │
│          │                 └─────────────┘               │         │
│          │                                                │         │
│          └────────────────────┬───────────────────────────┘         │
│                               │                                     │
│                               ▼                                     │
│                      ┌─────────────────┐                            │
│                      │  Slide Builder  │                            │
│                      │  (python-pptx)  │                            │
│                      └─────────────────┘                            │
│                               │                                     │
└───────────────────────────────┼─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                            Output                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  • presentation_YYYYMMDD_HHMMSS.pptx                                 │
│  • presentation_YYYYMMDD_HHMMSS.pdf (optional)                       │
│  • Generated images (if enabled)                                     │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Detailed Pipeline Flow

```
┌──────────────────────┐
│   User Input Text    │
│                      │
│ "Explain ML          │
│  * Supervised        │
│  * Unsupervised"     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│       STEP 1: Outline Parser             │
├──────────────────────────────────────────┤
│                                          │
│ • Detects input format                   │
│ • Parses structure                       │
│ • Creates slide scaffolding              │
│                                          │
│ Output: List[SlideData]                  │
│  - Slide 1: "Explain ML"                 │
│  - Slide 2: "Supervised"                 │
│  - Slide 3: "Unsupervised"               │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│     STEP 2: Content Generator            │
├──────────────────────────────────────────┤
│                                          │
│ For each slide:                          │
│  1. Generate expanded bullets            │
│     via LLM prompting                    │
│  2. Create speaker notes                 │
│  3. Generate image prompt                │
│                                          │
│ Uses: OpenAI API (or mock mode)         │
│                                          │
│ Output: Enhanced List[SlideData]         │
│  - Full bullets                          │
│  - Speaker notes                         │
│  - Image descriptions                    │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│      STEP 3: Image Generator             │
├──────────────────────────────────────────┤
│                                          │
│ For each slide:                          │
│  • Generate via DALL-E (if enabled)      │
│  • Or use placeholder images             │
│  • Save to output/images/                │
│                                          │
│ Output: List[SlideData] with images     │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│       STEP 4: Slide Builder              │
├──────────────────────────────────────────┤
│                                          │
│ • Create PowerPoint presentation         │
│ • Apply theme (colors, fonts)            │
│ • Add title slide                        │
│ • Add content slides with bullets        │
│ • Embed speaker notes                    │
│ • Place images (if available)            │
│ • Export to PDF (optional)               │
│                                          │
│ Uses: python-pptx library                │
│                                          │
│ Output: .pptx file (and .pdf if enabled) │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────┐
│   Generated Deck     │
│                      │
│ presentation.pptx    │
│ (Ready to download)  │
└──────────────────────┘
```

---

## Data Flow

```
Input Format               Parsed Structure           Expanded Content
─────────────             ──────────────────         ─────────────────

"Topic"                   SlideData {                SlideData {
                            title: "Topic"             title: "Topic"
or                          bullets: []                bullets: [
                          }                              "Point 1...",
"* Bullet 1"                                             "Point 2...",
"* Bullet 2"              SlideData {                    "Point 3..."
                            title: "Bullet 1"          ]
or                          bullets: []                speaker_notes: "..."
                          }                            image_prompt: "..."
"1. Section                                          }
   - Detail"              SlideData {
                            title: "Bullet 2"        [Same for each slide]
                            bullets: []
                          }
```

---

## Component Interaction

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  InputForm           SlidePreview         GenerateButton     │
│     │                    ▲                      │            │
│     │                    │                      │            │
│     └─── axios POST ─────┴──────── axios POST ──┘            │
│              │                          │                    │
└──────────────┼──────────────────────────┼────────────────────┘
               │                          │
               ▼                          ▼
         /preview                    /generate
               │                          │
┌──────────────┼──────────────────────────┼────────────────────┐
│              │      Backend (FastAPI)   │                    │
├──────────────┼──────────────────────────┼────────────────────┤
│              │                          │                    │
│         preview_slides()          generate_deck()            │
│              │                          │                    │
│              ├─── Parser ───────────────┤                    │
│              │                          │                    │
│              ├─── Generator ────────────┤                    │
│              │                          │                    │
│              │                    Image Generator            │
│              │                          │                    │
│              │                    Slide Builder              │
│              │                          │                    │
│              ▼                          ▼                    │
│         JSON response              File + JSON               │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

---

## Error Handling Flow

```
┌─────────────────────┐
│   User Request      │
└──────┬──────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  Validation (Pydantic)               │
│  ✓ Check input_text not empty        │
│  ✓ Validate options                  │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  Pipeline Execution                  │
│                                      │
│  Try:                                │
│    ✓ Parse outline                   │
│    ✓ Generate content (with retry)   │
│    ✓ Build slides                    │
│                                      │
│  Catch:                              │
│    ✗ OpenAI API error                │
│      → Use mock mode                 │
│    ✗ Invalid input                   │
│      → Return error                  │
│    ✗ File write error                │
│      → Return error                  │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────┐
│  Return Response     │
│  • Success + file    │
│  • Error + message   │
└──────────────────────┘
```

---

## Configuration Hierarchy

```
┌─────────────────────────────────────────────┐
│         Environment Variables                │
│  (Highest Priority)                         │
│                                             │
│  OPENAI_API_KEY, USE_DALLE, etc.            │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│         Request Parameters                   │
│  (Request-specific)                         │
│                                             │
│  theme, include_speaker_notes, etc.         │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│         Default Values                       │
│  (Lowest Priority)                          │
│                                             │
│  theme="professional", model="gpt-4o-mini"  │
└─────────────────────────────────────────────┘
```

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Production Setup                      │
├─────────────────────────────────────────────────────────┤
│                                                           │
│   Frontend (Vercel/Netlify)      Backend (AWS/GCP/Azure)│
│         │                                  │             │
│         │                                  │             │
│    HTTPS + CDN                      Docker Container    │
│         │                                  │             │
│         └──────────── HTTPS ───────────────┘             │
│                         │                                │
│                    API Gateway                           │
│                         │                                │
│                    Rate Limiting                         │
│                         │                                │
│                    Load Balancer                         │
│                                                           │
└───────────────────────────────────────────────────────────┘
```
