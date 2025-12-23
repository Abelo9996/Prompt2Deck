# Prompt2Deck Architecture

## System Design

Prompt2Deck follows a modular, pipeline-based architecture inspired by modern AI application design patterns. The system is split into clear, composable components that can be easily extended or replaced.

## High-Level Flow

```
User Input → Outline Parser → Content Generator → Image Generator → Slide Builder → PPTX Output
```

## Component Breakdown

### 1. Outline Parser (`outline_parser.py`)

**Purpose**: Convert raw text input into structured slide data.

**Input Types**:
- Simple topic (e.g., "Explain Machine Learning")
- Bullet list
- Nested outline

**Output**: List of `SlideData` objects with titles and initial bullets.

**Key Logic**:
- Detects input format using heuristics
- Parses hierarchical structure
- Creates initial slide scaffolding

### 2. Content Generator (`content_generator.py`)

**Purpose**: Use LLM to expand and enhance slide content.

**Features**:
- Expands bullet points into comprehensive talking points
- Generates speaker notes
- Creates image generation prompts
- Falls back to mock mode without API key

**LLM Integration**:
- Uses OpenAI API (GPT-4 or GPT-3.5-turbo)
- Async processing for efficiency
- Configurable model selection

### 3. Image Generator (`image_generator.py`)

**Purpose**: Generate or fetch images for each slide.

**Modes**:
- **DALL-E Mode**: Uses OpenAI's image generation API
- **Placeholder Mode**: Uses placeholder image services

**Features**:
- Downloads and saves images locally
- Safe filename generation
- Error handling with graceful fallback

### 4. Slide Builder (`slide_builder.py`)

**Purpose**: Assemble all components into a PowerPoint presentation.

**Features**:
- Uses `python-pptx` library
- Multiple theme support
- Custom formatting (fonts, colors, spacing)
- Speaker notes integration
- Optional PDF export

**Themes**:
- Professional (corporate blue)
- Modern (bright and bold)
- Minimal (black and white)

## API Layer

### FastAPI Server (`main.py`)

**Endpoints**:
- `GET /`: Health check
- `POST /preview`: Preview slide structure
- `POST /generate`: Generate complete deck
- `GET /download/{filename}`: Download file

**Features**:
- Async/await for better performance
- CORS support for web frontend
- Error handling and validation
- File management

## Data Models (`models.py`)

### Core Models

```python
SlideData           # Single slide with content
PreviewRequest      # API request for preview
PreviewResponse     # API response with slide data
GenerateRequest     # API request for generation
GenerateResponse    # API response with file paths
OutlineSection      # Internal outline representation
```

All models use Pydantic for validation and serialization.

## Frontend Architecture

### Next.js Application

**Pages**:
- `index.tsx`: Main application page

**Components**:
- `InputForm`: Text input and preview trigger
- `SlidePreview`: Visual preview of slides
- `GenerateButton`: Configuration and generation

**State Management**:
- React hooks for local state
- Axios for API communication

**Styling**:
- Tailwind CSS for responsive design
- Custom color scheme matching backend themes

## Configuration

### Environment-Based

**Backend**:
- `OPENAI_API_KEY`: LLM access
- `OPENAI_MODEL`: Model selection
- `USE_DALLE`: Enable image generation
- `HOST`, `PORT`: Server configuration

**Frontend**:
- `NEXT_PUBLIC_API_URL`: Backend endpoint

### Feature Flags

- Mock mode (no API key needed)
- Image generation (optional)
- PDF export (requires LibreOffice)
- Theme selection

## Extension Points

### Adding New Input Formats

Extend `OutlineParser` class:
```python
async def _parse_custom_format(self, text: str) -> List[SlideData]:
    # Custom parsing logic
    pass
```

### Adding New Themes

Add to `themes` dict in `SlideBuilder`:
```python
"custom_theme": {
    "title_color": RGBColor(...),
    "text_color": RGBColor(...),
    "background": RGBColor(...),
    "accent": RGBColor(...)
}
```

### Adding New LLM Providers

Extend `ContentGenerator`:
```python
async def _call_alternative_llm(self, prompt: str) -> str:
    # Integration with Anthropic, Cohere, etc.
    pass
```

### Adding Google Slides Support

Create new builder class:
```python
class GoogleSlidesBuilder:
    async def build_deck(self, slides: List[SlideData]):
        # Use Google Slides API
        pass
```

## Performance Considerations

### Async Processing

- All I/O operations are async
- Parallel slide processing where possible
- Non-blocking API endpoints

### Caching

- Image caching in output directory
- Reuse generated content when possible

### Rate Limiting

- Consider adding rate limits for API calls
- Batch LLM requests when feasible

## Security Considerations

### API Keys

- Store in environment variables
- Never commit to version control
- Validate before use

### File System

- Sanitize user input for filenames
- Limit output directory access
- Clean up old files periodically

### CORS

- Configure appropriately for production
- Restrict origins in deployment

## Deployment Recommendations

### Backend

- Use Docker for containerization
- Deploy on cloud platforms (AWS, GCP, Azure)
- Set up proper logging and monitoring
- Use gunicorn or similar for production

### Frontend

- Deploy on Vercel, Netlify, or similar
- Configure environment variables
- Set up CI/CD pipeline
- Enable analytics

### Full Stack

- Use nginx as reverse proxy
- Set up SSL certificates
- Configure proper CORS policies
- Implement authentication if needed

## Monitoring & Logging

### Key Metrics

- API response times
- LLM call success rates
- File generation success rates
- Error rates by endpoint

### Logging

- Structured logging with levels
- Request/response logging
- Error tracking
- Performance monitoring

## Testing Strategy

### Unit Tests

- Test each pipeline component independently
- Mock external API calls
- Test edge cases and error handling

### Integration Tests

- Test full pipeline flow
- Test API endpoints
- Test file generation

### Example

```python
async def test_outline_parser():
    parser = OutlineParser()
    slides = await parser.parse("Simple topic")
    assert len(slides) > 0
    assert slides[0].title is not None
```

## Future Architecture Enhancements

- Message queue for long-running tasks
- WebSocket support for real-time updates
- Database for user sessions and history
- Template marketplace
- Collaborative editing features
