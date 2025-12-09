"""
Image Generator Module
Generates images or icons for slides using AI or placeholder graphics.
"""

import os
import hashlib
from typing import List, Optional
from openai import AsyncOpenAI
import httpx
from models import SlideData


class ImageGenerator:
    """
    Generates images for slides using OpenAI DALL-E or placeholder images.
    Falls back to placeholder mode if API key is not available.
    """
    
    def __init__(self):
        """Initialize the image generator."""
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = AsyncOpenAI(api_key=api_key) if api_key else None
        self.use_dalle = os.getenv("USE_DALLE", "false").lower() == "true"
        self.image_dir = os.path.join(os.path.dirname(__file__), "..", "output", "images")
        os.makedirs(self.image_dir, exist_ok=True)
    
    async def generate_images(self, slides: List[SlideData]) -> List[SlideData]:
        """
        Generate images for all slides.
        
        Args:
            slides: List of slides with image prompts
            
        Returns:
            List of slides with image_path populated
        """
        slides_with_images = []
        
        for slide in slides:
            if slide.image_prompt:
                image_path = await self._generate_single_image(
                    slide.image_prompt,
                    slide.title
                )
                slide.image_path = image_path
            
            slides_with_images.append(slide)
        
        return slides_with_images
    
    async def _generate_single_image(
        self,
        prompt: str,
        title: str
    ) -> Optional[str]:
        """
        Generate a single image.
        
        Args:
            prompt: Image generation prompt
            title: Slide title (for filename)
            
        Returns:
            Path to generated image or None
        """
        if self.use_dalle and self.client:
            return await self._generate_dalle_image(prompt, title)
        else:
            return await self._generate_placeholder_image(title)
    
    async def _generate_dalle_image(
        self,
        prompt: str,
        title: str
    ) -> Optional[str]:
        """Generate image using DALL-E API."""
        try:
            # Enhance prompt for better results
            enhanced_prompt = f"Simple, professional, minimalist icon or illustration: {prompt}. Clean design, no text, suitable for presentation slide."
            
            response = await self.client.images.generate(
                model="dall-e-3",
                prompt=enhanced_prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            image_url = response.data[0].url
            
            # Download the image
            filename = self._generate_filename(title)
            filepath = os.path.join(self.image_dir, filename)
            
            async with httpx.AsyncClient() as client:
                img_response = await client.get(image_url)
                img_response.raise_for_status()
                
                with open(filepath, 'wb') as f:
                    f.write(img_response.content)
            
            return filepath
            
        except Exception as e:
            print(f"Error generating DALL-E image for '{title}': {e}")
            return await self._generate_placeholder_image(title)
    
    async def _generate_placeholder_image(self, title: str) -> Optional[str]:
        """
        Generate a placeholder image URL using a public service.
        
        Args:
            title: Slide title
            
        Returns:
            Path/URL to placeholder image
        """
        # Use a placeholder image service
        # In production, you might want to generate actual placeholder images
        
        # Create a simple identifier from the title
        identifier = hashlib.md5(title.encode()).hexdigest()[:8]
        
        # For now, return a placeholder URL (could be used directly in slides)
        # Alternatively, download and save placeholder images
        placeholder_url = f"https://via.placeholder.com/800x450/4A90E2/FFFFFF?text={title[:20].replace(' ', '+')}"
        
        # In a real implementation, you might download this
        # For now, return the URL which can be used by the slide builder
        return placeholder_url
    
    def _generate_filename(self, title: str) -> str:
        """Generate a safe filename from slide title."""
        # Remove special characters and limit length
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_'))
        safe_title = safe_title.replace(' ', '_')[:50]
        
        # Add hash to ensure uniqueness
        title_hash = hashlib.md5(title.encode()).hexdigest()[:8]
        
        return f"{safe_title}_{title_hash}.png"
