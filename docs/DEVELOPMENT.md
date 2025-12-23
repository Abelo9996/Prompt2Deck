# Development Guide

This guide helps developers understand, extend, and contribute to Prompt2Deck.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Development Setup](#development-setup)
3. [Architecture Overview](#architecture-overview)
4. [Adding Features](#adding-features)
5. [Testing](#testing)
6. [Debugging](#debugging)
7. [Best Practices](#best-practices)

---

## Project Structure

```
Prompt2Deck/
├── backend/              # Python FastAPI backend
│   ├── pipeline/         # Core processing modules
│   ├── main.py          # API server
│   ├── models.py        # Data models
│   └── test_pipeline.py # Test script
├── frontend/            # Next.js frontend
│   ├── pages/          # Next.js pages
│   ├── components/     # React components
│   └── styles/         # CSS files
├── examples/           # Documentation and examples
├── docs/              # Additional documentation
└── tests/             # Test suite (to be added)
```

---

## Development Setup

### Prerequisites

Install required tools:
```bash
# Python
python3 --version  # Should be 3.10+

# Node.js
node --version     # Should be 18+
npm --version

# Git
git --version
```

### Initial Setup

1. Clone and setup:
```bash
git clone <repo-url>
cd Prompt2Deck
./setup.sh  # or setup.bat on Windows
```

2. Configure environment:
```bash
# Backend
cd backend
cp .env.example .env
# Edit .env with your OpenAI API key

# Frontend
cd ../frontend
cp .env.example .env.local
```

3. Start development servers:
```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
python main.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

---

## Architecture Overview

### Backend Pipeline

The backend follows a pipeline architecture:

```python
Input → Parser → Generator → Image Gen → Builder → Output
```

Each component is:
- **Async**: Non-blocking operations
- **Modular**: Can be tested independently
- **Extensible**: Easy to add new functionality

### Key Components

#### 1. Outline Parser
```python
class OutlineParser:
    async def parse(self, input_text: str) -> List[SlideData]:
        # Convert text to structured slides
        pass
```

**Responsibilities**:
- Detect input format
- Parse structure
- Create slide scaffolding

#### 2. Content Generator
```python
class ContentGenerator:
    async def expand_slides(self, slides: List[SlideData]) -> List[SlideData]:
        # Enhance slides with LLM
        pass
```

**Responsibilities**:
- Expand bullet points
- Generate speaker notes
- Create image prompts

#### 3. Image Generator
```python
class ImageGenerator:
    async def generate_images(self, slides: List[SlideData]) -> List[SlideData]:
        # Add images to slides
        pass
```

**Responsibilities**:
- Generate via DALL-E
- Handle placeholders
- Manage image files

#### 4. Slide Builder
```python
class SlideBuilder:
    async def build_deck(self, slides: List[SlideData]) -> str:
        # Create PPTX file
        pass
```

**Responsibilities**:
- Create PowerPoint
- Apply themes
- Export to PDF

---

## Adding Features

### Adding a New Input Format

1. Edit `outline_parser.py`:

```python
def _is_custom_format(self, text: str) -> bool:
    """Detect custom format."""
    return text.startswith("CUSTOM:")

async def _parse_custom_format(self, text: str) -> List[SlideData]:
    """Parse custom format."""
    # Your parsing logic
    pass
```

2. Update the `parse` method:

```python
async def parse(self, input_text: str) -> List[SlideData]:
    if self._is_custom_format(input_text):
        return await self._parse_custom_format(input_text)
    # ... existing logic
```

### Adding a New Theme

1. Edit `slide_builder.py`:

```python
self.themes = {
    # Existing themes...
    "custom": {
        "title_color": RGBColor(255, 0, 0),
        "text_color": RGBColor(0, 0, 0),
        "background": RGBColor(255, 255, 255),
        "accent": RGBColor(0, 0, 255)
    }
}
```

2. Update frontend theme selector in `GenerateButton.tsx`:

```typescript
<option value="custom">Custom</option>
```

### Adding a New LLM Provider

1. Create a new generator class:

```python
class AnthropicGenerator(ContentGenerator):
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    async def _generate_bullets(self, title: str, bullets: List[str]) -> List[str]:
        # Use Anthropic API
        pass
```

2. Make it configurable:

```python
# In main.py
llm_provider = os.getenv("LLM_PROVIDER", "openai")
if llm_provider == "anthropic":
    content_generator = AnthropicGenerator()
else:
    content_generator = ContentGenerator()
```

### Adding a New API Endpoint

1. Add endpoint in `main.py`:

```python
@app.post("/custom-endpoint")
async def custom_endpoint(request: CustomRequest):
    """Custom endpoint description."""
    try:
        # Your logic
        return CustomResponse(...)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

2. Add models in `models.py`:

```python
class CustomRequest(BaseModel):
    field1: str
    field2: int

class CustomResponse(BaseModel):
    result: str
```

3. Update frontend to use it:

```typescript
const response = await axios.post(`${API_URL}/custom-endpoint`, {
  field1: "value",
  field2: 123
})
```

---

## Testing

### Running Tests

```bash
cd backend
pytest
pytest --cov  # With coverage
```

### Writing Tests

Create test files in `tests/` directory:

```python
# tests/test_parser.py
import pytest
from pipeline.outline_parser import OutlineParser

@pytest.mark.asyncio
async def test_simple_topic():
    parser = OutlineParser()
    slides = await parser.parse("Test Topic")
    assert len(slides) > 0
    assert slides[0].title == "Test Topic"

@pytest.mark.asyncio
async def test_bullet_list():
    parser = OutlineParser()
    input_text = "* Point 1\n* Point 2"
    slides = await parser.parse(input_text)
    assert len(slides) == 2
```

### Manual Testing

Use the test script:
```bash
cd backend
python test_pipeline.py
```

Test the API:
```bash
curl -X POST http://localhost:8000/preview \
  -H "Content-Type: application/json" \
  -d '{"input_text": "Test", "include_speaker_notes": true}'
```

---

## Debugging

### Backend Debugging

1. **Enable verbose logging**:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

2. **Use Python debugger**:

```python
import pdb; pdb.set_trace()
```

3. **Check logs**:

```bash
# In main.py, FastAPI logs to console
python main.py  # Watch for errors
```

### Frontend Debugging

1. **Browser DevTools**: Open Chrome DevTools (F12)

2. **Console logging**:

```typescript
console.log('Debug info:', data)
```

3. **Network tab**: Check API requests and responses

### Common Issues

**Issue**: Import errors
```bash
# Solution: Ensure virtual environment is activated
source venv/bin/activate
```

**Issue**: Module not found
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue**: API connection refused
```bash
# Solution: Check backend is running
curl http://localhost:8000/
```

---

## Best Practices

### Code Style

**Python**:
- Follow PEP 8
- Use type hints
- Write docstrings
- Use async/await for I/O

```python
async def process_data(input: str, options: Dict[str, Any]) -> List[Result]:
    """
    Process input data with options.
    
    Args:
        input: Raw input string
        options: Processing options
        
    Returns:
        List of processed results
    """
    # Implementation
    pass
```

**TypeScript**:
- Use interfaces for props
- Functional components
- Destructure props
- Use TypeScript strictly

```typescript
interface ComponentProps {
  title: string
  onAction: () => void
  optional?: boolean
}

export default function Component({ title, onAction, optional }: ComponentProps) {
  return <div>{title}</div>
}
```

### Error Handling

Always handle errors gracefully:

```python
try:
    result = await dangerous_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    # Fallback behavior
    result = fallback_operation()
```

### Async Best Practices

```python
# Good: Parallel execution
async def process_all(items):
    tasks = [process_item(item) for item in items]
    results = await asyncio.gather(*tasks)
    return results

# Bad: Sequential execution
async def process_all_slow(items):
    results = []
    for item in items:
        result = await process_item(item)
        results.append(result)
    return results
```

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes
git add .
git commit -m "Add new feature"

# Push and create PR
git push origin feature/new-feature
```

### Commit Messages

Follow conventional commits:
```
feat: Add new theme support
fix: Fix image generation error
docs: Update README
refactor: Simplify parser logic
test: Add tests for content generator
```

---

## Performance Tips

1. **Use async/await** for all I/O operations
2. **Batch LLM calls** when possible
3. **Cache results** where appropriate
4. **Limit output size** for large presentations
5. **Use streaming** for large responses

---

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [python-pptx Documentation](https://python-pptx.readthedocs.io/)
- [OpenAI API Documentation](https://platform.openai.com/docs)

---

## Getting Help

1. Check documentation files
2. Review example code
3. Open an issue on GitHub
4. Join community discussions

---

Happy coding! 🚀
