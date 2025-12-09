"""
Prompt2Deck FastAPI Server
Main entry point for the slide deck generation service.
"""

import os
from typing import Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from models import (
    GenerateRequest,
    PreviewRequest,
    GenerateResponse,
    PreviewResponse,
    SlideData
)
from pipeline.outline_parser import OutlineParser
from pipeline.content_generator import ContentGenerator
from pipeline.image_generator import ImageGenerator
from pipeline.slide_builder import SlideBuilder

app = FastAPI(
    title="Prompt2Deck API",
    description="AI-powered slide deck generation service",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize pipeline components
outline_parser = OutlineParser()
content_generator = ContentGenerator()
image_generator = ImageGenerator()
slide_builder = SlideBuilder()

# Ensure output directory exists
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "service": "Prompt2Deck API",
        "version": "1.0.0"
    }


@app.post("/preview", response_model=PreviewResponse)
async def preview_slides(request: PreviewRequest):
    """
    Generate a preview of the slide structure without creating the actual deck.
    
    Args:
        request: PreviewRequest containing the input text/outline
        
    Returns:
        PreviewResponse with structured slide data
    """
    try:
        # Parse outline into slide structure
        slides = await outline_parser.parse(request.input_text)
        
        # Expand content for each slide
        expanded_slides = await content_generator.expand_slides(
            slides,
            include_speaker_notes=request.include_speaker_notes
        )
        
        return PreviewResponse(
            slides=expanded_slides,
            total_slides=len(expanded_slides)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preview generation failed: {str(e)}")


@app.post("/generate", response_model=GenerateResponse)
async def generate_deck(request: GenerateRequest):
    """
    Generate a complete slide deck from input text/outline.
    
    Args:
        request: GenerateRequest containing the input text and options
        
    Returns:
        GenerateResponse with download URL and metadata
    """
    try:
        # Step 1: Parse outline into slide structure
        slides = await outline_parser.parse(request.input_text)
        
        # Step 2: Expand content for each slide
        expanded_slides = await content_generator.expand_slides(
            slides,
            include_speaker_notes=request.include_speaker_notes
        )
        
        # Step 3: Generate images for each slide (if enabled)
        if request.generate_images:
            slides_with_images = await image_generator.generate_images(expanded_slides)
        else:
            slides_with_images = expanded_slides
        
        # Step 4: Build the slide deck
        output_path = await slide_builder.build_deck(
            slides_with_images,
            output_dir=OUTPUT_DIR,
            theme=request.theme
        )
        
        # Step 5: Export to PDF if requested
        pdf_path = None
        if request.export_pdf:
            pdf_path = await slide_builder.export_to_pdf(output_path)
        
        return GenerateResponse(
            file_path=output_path,
            pdf_path=pdf_path,
            total_slides=len(slides_with_images),
            message="Deck generated successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deck generation failed: {str(e)}")


@app.get("/download/{filename}")
async def download_file(filename: str):
    """
    Download a generated file.
    
    Args:
        filename: Name of the file to download
        
    Returns:
        FileResponse with the requested file
    """
    file_path = os.path.join(OUTPUT_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
