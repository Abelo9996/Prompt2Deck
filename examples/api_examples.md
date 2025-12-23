# API Testing Guide

## Quick Start

1. Start the backend server:
```bash
cd backend
python main.py
```

2. Test the health endpoint:
```bash
curl http://localhost:8000/
```

## API Endpoints

### GET /
Health check endpoint.

**Response:**
```json
{
  "status": "online",
  "service": "Prompt2Deck API",
  "version": "1.0.0"
}
```

---

### POST /preview
Generate a preview of slides without creating the deck.

**Request Body:**
```json
{
  "input_text": "Your topic or outline here",
  "include_speaker_notes": true
}
```

**Response:**
```json
{
  "slides": [
    {
      "title": "Slide Title",
      "bullets": ["Point 1", "Point 2"],
      "speaker_notes": "Notes for the presenter",
      "image_prompt": "Description for image generation"
    }
  ],
  "total_slides": 5
}
```

---

### POST /generate
Generate a complete slide deck.

**Request Body:**
```json
{
  "input_text": "Your topic or outline here",
  "include_speaker_notes": true,
  "generate_images": false,
  "export_pdf": false,
  "theme": "professional"
}
```

**Response:**
```json
{
  "file_path": "/path/to/presentation_20231201_120000.pptx",
  "pdf_path": null,
  "total_slides": 5,
  "message": "Deck generated successfully"
}
```

---

### GET /download/{filename}
Download a generated file.

**Example:**
```bash
curl http://localhost:8000/download/presentation_20231201_120000.pptx -O
```

---

## Testing with Python

```python
import requests

API_URL = "http://localhost:8000"

# Preview slides
response = requests.post(f"{API_URL}/preview", json={
    "input_text": "Introduction to AI",
    "include_speaker_notes": True
})
print(response.json())

# Generate deck
response = requests.post(f"{API_URL}/generate", json={
    "input_text": "Introduction to AI",
    "include_speaker_notes": True,
    "generate_images": False,
    "export_pdf": False,
    "theme": "professional"
})

# Download the generated file
filename = response.json()["file_path"].split("/")[-1]
file_response = requests.get(f"{API_URL}/download/{filename}")

with open(filename, "wb") as f:
    f.write(file_response.content)
```
