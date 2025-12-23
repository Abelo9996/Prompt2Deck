# Prompt2Deck ✨

> Transform plain text into professional slide decks with AI

An AI-powered presentation generator that converts topics, outlines, or bullet points into polished PowerPoint presentations in seconds.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)

## 🎯 Features

- **🤖 AI-Powered Content** - Automatically expands outlines into comprehensive slides using GPT
- **📝 Multiple Input Formats** - Simple topics, bullet lists, or nested outlines
- **🎨 Professional Themes** - Choose from Modern, Professional, or Minimal designs
- **🗣️ Speaker Notes** - Auto-generated presentation guidance
- **🖼️ Image Support** - Optional DALL-E integration for slide visuals
- **📄 Export Options** - PPTX and PDF formats
- **🌐 Web Interface** - User-friendly Next.js frontend
- **🚀 Fast API** - RESTful endpoints for programmatic access
- **💰 Cost-Effective** - ~$0.01-0.05 per presentation with GPT-4o-mini

## 📸 Demo

```
Input:
  Introduction to Machine Learning
  * What is ML?
  * Types of Learning
  * Real-world Applications

Output:
  → Professional PPTX with 4 slides
  → AI-expanded content
  → Speaker notes
  → Ready to present!
```

## 🚀 Quick Start

### Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/Abelo9996/Prompt2Deck.git
cd Prompt2Deck

# Run setup script
./setup.sh  # macOS/Linux
# or
setup.bat   # Windows

# Add your OpenAI API key
cd backend
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=your_key_here

# Start the backend
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend (Optional Web UI)

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000` in your browser

### Manual Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Add your OpenAI API key to .env
python main.py
```

## 💻 Usage

### Web Interface

1. Open `http://localhost:3000`
2. Enter your content (topic, bullets, or outline)
3. Click **"Preview Slides"** to see the structure
4. Configure options (speaker notes, theme)
5. Click **"Generate Deck"**
6. Download your PPTX file

### API Examples

**Preview Slides:**
```bash
curl -X POST http://localhost:8000/preview \
  -H "Content-Type: application/json" \
  -d '{"input_text": "Machine Learning Basics", "include_speaker_notes": true}'
```

**Generate Presentation:**
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "Introduction to AI\n* What is AI?\n* Applications\n* Future",
    "include_speaker_notes": true,
    "theme": "professional"
  }'
```

**Python Client:**
```python
import requests

response = requests.post("http://localhost:8000/generate", json={
    "input_text": "Cloud Computing\n* IaaS\n* PaaS\n* SaaS",
    "include_speaker_notes": True,
    "theme": "modern"
})

file_path = response.json()["file_path"]
print(f"✅ Deck created: {file_path}")
```

## 📝 Input Formats

### Simple Topic
```
Explain Large Language Models
```
→ Auto-generates complete presentation structure

### Bullet List
```
Introduction to Cloud Computing
* Infrastructure as a Service
* Platform as a Service
* Software as a Service
```
→ Each bullet becomes a slide

### Nested Outline
```
Machine Learning Basics

1. Introduction
   - What is ML?
   - Why it matters

2. Types of Learning
   - Supervised
   - Unsupervised
```
→ Full control over slide structure

📚 See [`examples/sample_inputs.md`](examples/sample_inputs.md) for more examples

## 🏗️ Architecture

```
Prompt2Deck/
├── backend/              # FastAPI Python backend
│   ├── main.py          # API server
│   ├── models.py        # Data models
│   └── pipeline/        # Processing pipeline
│       ├── outline_parser.py      # Parse input formats
│       ├── content_generator.py   # LLM content expansion
│       ├── image_generator.py     # Image generation
│       └── slide_builder.py       # PPTX assembly
├── frontend/            # Next.js web interface
│   ├── pages/          # Routes
│   └── components/     # React components
├── examples/           # Sample inputs
└── docs/              # Documentation

```

**Pipeline:** Input → Parse → Generate → Build → Export

📖 See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for detailed design

## ⚙️ Configuration

### Backend Environment (`backend/.env`)

```bash
# Required for AI content (or use mock mode)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# Optional features
USE_DALLE=false          # Enable DALL-E images (costs extra)
HOST=0.0.0.0
PORT=8000
```

### Frontend Environment (`frontend/.env.local`)

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Features

| Feature | Status | Notes |
|---------|--------|-------|
| AI Content | ✅ | Requires OpenAI API key |
| Mock Mode | ✅ | Works without API key |
| Themes | ✅ | Professional, Modern, Minimal |
| Speaker Notes | ✅ | Auto-generated |
| DALL-E Images | 🔧 | Optional, set `USE_DALLE=true` |
| PDF Export | 🔧 | Optional, requires LibreOffice |

## 📡 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/preview` | Preview slide structure |
| `POST` | `/generate` | Generate PPTX deck |
| `GET` | `/download/{filename}` | Download file |

📚 Full API docs: [`examples/api_examples.md`](examples/api_examples.md)

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3.10+, FastAPI, python-pptx |
| Frontend | Next.js 14, React 18, TypeScript, Tailwind CSS |
| AI | OpenAI GPT-4o-mini / GPT-4 |
| Images | DALL-E 3 (optional) |
| Styling | Tailwind CSS |

## 🧪 Development

```bash
# Run tests
cd backend
pytest

# Format code
black .

# Type checking
mypy .
```

**Adding Custom Themes:**
Edit `backend/pipeline/slide_builder.py`:
```python
"custom": {
    "title_color": RGBColor(r, g, b),
    "text_color": RGBColor(r, g, b),
}
```

📖 See [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md) for full guide

## 🗺️ Roadmap

- [ ] Google Slides API integration
- [ ] Batch processing for multiple decks
- [ ] Custom template marketplace
- [ ] Real-time collaboration
- [ ] Markdown export
- [ ] Notion/Docs integration

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| API key not found | Add `OPENAI_API_KEY` to `backend/.env` |
| Quota exceeded | Add credits at [platform.openai.com](https://platform.openai.com/account/billing) |
| Module not found | Run `pip install -r requirements.txt` |
| PDF export fails | Install LibreOffice: `brew install libreoffice` |
| Port in use | Change `PORT` in `backend/.env` |

📚 More help: [`docs/OPENAI_QUOTA_FIX.md`](docs/OPENAI_QUOTA_FIX.md)

## 🤝 Contributing

Contributions are welcome! Please see [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Show Your Support

If you find this project helpful, please consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting new features
- 🔀 Contributing code

## 📬 Contact

For questions or feedback, please [open an issue](https://github.com/Abelo9996/Prompt2Deck/issues).

---

<p align="center">
  <strong>Built with ❤️ using AI and modern web technologies</strong><br>
  Made by <a href="https://github.com/Abelo9996">@Abelo9996</a>
</p>
