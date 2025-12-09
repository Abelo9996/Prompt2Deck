"""
Content Generator Module
Uses LLM to expand slide content and generate speaker notes.
"""

import os
from typing import List, Optional
from openai import AsyncOpenAI
from models import SlideData


class ContentGenerator:
    """
    Generates expanded content for slides using an LLM.
    Expands bullet points and creates speaker notes.
    """
    
    def __init__(self):
        """Initialize the content generator with OpenAI client."""
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = AsyncOpenAI(api_key=api_key) if api_key else None
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.use_mock = not api_key  # Use mock mode if no API key
    
    async def expand_slides(
        self,
        slides: List[SlideData],
        include_speaker_notes: bool = True
    ) -> List[SlideData]:
        """
        Expand content for all slides.
        
        Args:
            slides: List of slides with basic structure
            include_speaker_notes: Whether to generate speaker notes
            
        Returns:
            List of slides with expanded content
        """
        expanded_slides = []
        
        for slide in slides:
            expanded_slide = await self._expand_single_slide(
                slide,
                include_speaker_notes
            )
            expanded_slides.append(expanded_slide)
        
        return expanded_slides
    
    async def _expand_single_slide(
        self,
        slide: SlideData,
        include_speaker_notes: bool
    ) -> SlideData:
        """
        Expand content for a single slide.
        
        Args:
            slide: Slide to expand
            include_speaker_notes: Whether to generate speaker notes
            
        Returns:
            Slide with expanded content
        """
        if self.use_mock:
            return self._mock_expand_slide(slide, include_speaker_notes)
        
        try:
            # Generate expanded bullets
            bullets = await self._generate_bullets(slide.title, slide.bullets)
            
            # Generate speaker notes if requested
            speaker_notes = None
            if include_speaker_notes:
                speaker_notes = await self._generate_speaker_notes(
                    slide.title,
                    bullets
                )
            
            # Generate image prompt
            image_prompt = await self._generate_image_prompt(slide.title, bullets)
            
            return SlideData(
                title=slide.title,
                bullets=bullets,
                speaker_notes=speaker_notes,
                image_prompt=image_prompt
            )
            
        except Exception as e:
            print(f"Error expanding slide '{slide.title}': {e}")
            return self._mock_expand_slide(slide, include_speaker_notes)
    
    async def _generate_bullets(
        self,
        title: str,
        existing_bullets: List[str]
    ) -> List[str]:
        """Generate or expand bullet points for a slide."""
        if not self.client:
            return existing_bullets or [f"Key point about {title}"]
        
        context = "\n".join(f"- {b}" for b in existing_bullets) if existing_bullets else ""
        
        prompt = f"""Generate 3-5 concise, high-quality bullet points for a slide titled "{title}".

{f"Existing context:{context}" if context else ""}

Requirements:
- Each bullet should be clear and actionable
- Keep bullets concise (max 10-15 words each)
- Focus on key insights and takeaways
- Use professional language

Return only the bullet points, one per line, without bullet markers."""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert presentation designer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        
        content = response.choices[0].message.content.strip()
        bullets = [line.strip() for line in content.split('\n') if line.strip()]
        
        return bullets[:5]  # Limit to 5 bullets
    
    async def _generate_speaker_notes(
        self,
        title: str,
        bullets: List[str]
    ) -> str:
        """Generate speaker notes for a slide."""
        if not self.client:
            return f"Speaker notes for: {title}"
        
        bullets_text = "\n".join(f"- {b}" for b in bullets)
        
        prompt = f"""Generate concise speaker notes for a slide titled "{title}" with these bullet points:

{bullets_text}

Requirements:
- 2-3 sentences maximum
- Provide context and elaboration on the bullets
- Use conversational tone suitable for presenting
- Focus on what to emphasize when presenting

Return only the speaker notes text."""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert presentation coach."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        return response.choices[0].message.content.strip()
    
    async def _generate_image_prompt(self, title: str, bullets: List[str]) -> str:
        """Generate a prompt for image generation."""
        if not self.client:
            return f"Professional icon or illustration representing {title}"
        
        bullets_text = ", ".join(bullets[:3])
        
        prompt = f"""Create a concise image generation prompt for a slide titled "{title}" about: {bullets_text}

Requirements:
- Describe a simple, professional icon or illustration
- Should be clean and minimalist
- Avoid text or complex scenes
- 1-2 sentences maximum

Return only the image prompt."""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert visual designer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=100
        )
        
        return response.choices[0].message.content.strip()
    
    def _mock_expand_slide(
        self,
        slide: SlideData,
        include_speaker_notes: bool
    ) -> SlideData:
        """Create mock expanded content when API is unavailable."""
        bullets = slide.bullets if slide.bullets else [
            f"Key insight about {slide.title}",
            f"Important consideration for {slide.title}",
            f"Practical application of {slide.title}"
        ]
        
        speaker_notes = None
        if include_speaker_notes:
            speaker_notes = f"When presenting this slide, emphasize the key concepts of {slide.title} and how they relate to the overall topic."
        
        return SlideData(
            title=slide.title,
            bullets=bullets,
            speaker_notes=speaker_notes,
            image_prompt=f"Professional icon representing {slide.title}"
        )
