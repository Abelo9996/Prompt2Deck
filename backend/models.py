"""
Data models for the Prompt2Deck API.
Defines request/response schemas and internal data structures.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class SlideData(BaseModel):
    """Represents a single slide with its content."""
    
    title: str = Field(..., description="Slide title")
    bullets: List[str] = Field(default_factory=list, description="List of bullet points")
    speaker_notes: Optional[str] = Field(None, description="Optional speaker notes")
    image_path: Optional[str] = Field(None, description="Path to generated image")
    image_prompt: Optional[str] = Field(None, description="Prompt used for image generation")


class PreviewRequest(BaseModel):
    """Request model for slide preview endpoint."""
    
    input_text: str = Field(..., description="Input text, topic, or outline")
    include_speaker_notes: bool = Field(default=True, description="Generate speaker notes")


class PreviewResponse(BaseModel):
    """Response model for slide preview endpoint."""
    
    slides: List[SlideData] = Field(..., description="List of slide data")
    total_slides: int = Field(..., description="Total number of slides")


class GenerateRequest(BaseModel):
    """Request model for deck generation endpoint."""
    
    input_text: str = Field(..., description="Input text, topic, or outline")
    include_speaker_notes: bool = Field(default=True, description="Generate speaker notes")
    generate_images: bool = Field(default=True, description="Generate images for slides")
    export_pdf: bool = Field(default=False, description="Export to PDF in addition to PPTX")
    theme: str = Field(default="professional", description="Slide deck theme")


class GenerateResponse(BaseModel):
    """Response model for deck generation endpoint."""
    
    file_path: str = Field(..., description="Path to generated PPTX file")
    pdf_path: Optional[str] = Field(None, description="Path to generated PDF file")
    total_slides: int = Field(..., description="Total number of slides")
    message: str = Field(..., description="Status message")


class OutlineSection(BaseModel):
    """Internal model for parsed outline sections."""
    
    title: str
    sub_points: List[str] = Field(default_factory=list)
    depth: int = Field(default=0, description="Nesting depth in outline")
