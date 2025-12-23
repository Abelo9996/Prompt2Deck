"""
Outline Parser Module
Converts raw text input into structured slide sections.
"""

import re
from typing import List
from models import SlideData, OutlineSection


class OutlineParser:
    """
    Parses various input formats into structured slide data.
    Supports:
    - Simple topics (generates outline)
    - Bullet lists
    - Nested outlines
    """
    
    def __init__(self):
        self.min_slides = 3
        self.max_slides = 20
    
    async def parse(self, input_text: str) -> List[SlideData]:
        """
        Parse input text into a list of slide structures.
        
        Args:
            input_text: Raw input from user
            
        Returns:
            List of SlideData objects with titles and initial bullets
        """
        input_text = input_text.strip()
        
        # Detect input type and parse accordingly
        if self._is_simple_topic(input_text):
            return await self._parse_simple_topic(input_text)
        elif self._is_bulleted_list(input_text):
            return await self._parse_bulleted_list(input_text)
        else:
            return await self._parse_nested_outline(input_text)
    
    def _is_simple_topic(self, text: str) -> bool:
        """Check if input is a simple topic/question."""
        lines = text.strip().split('\n')
        return len(lines) <= 2 and not any(c in text for c in ['*', '-', '•', '1.', '2.'])
    
    def _is_bulleted_list(self, text: str) -> bool:
        """Check if input is a simple bulleted list."""
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        bullet_chars = ['*', '-', '•']
        bulleted_lines = sum(1 for l in lines if any(l.startswith(c) for c in bullet_chars))
        return bulleted_lines >= len(lines) * 0.7
    
    async def _parse_simple_topic(self, topic: str) -> List[SlideData]:
        """
        Generate a slide structure from a simple topic.
        Creates a basic outline: Title, Introduction, Key Points, Conclusion.
        """
        slides = [
            SlideData(
                title=topic,
                bullets=["Overview", "Key Concepts", "Applications"]
            ),
            SlideData(
                title="Introduction",
                bullets=[f"Understanding {topic}", "Context and Background"]
            ),
            SlideData(
                title="Key Concepts",
                bullets=["Concept 1", "Concept 2", "Concept 3"]
            ),
            SlideData(
                title="Applications",
                bullets=["Real-world use cases", "Practical examples"]
            ),
            SlideData(
                title="Conclusion",
                bullets=["Summary", "Key Takeaways", "Next Steps"]
            )
        ]
        return slides
    
    async def _parse_bulleted_list(self, text: str) -> List[SlideData]:
        """
        Parse a simple bulleted list into slides.
        Each bullet becomes a slide title.
        """
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        slides = []
        
        # Add title slide if first line looks like a title
        first_line = lines[0]
        if not any(first_line.startswith(c) for c in ['*', '-', '•', '1.', '2.']):
            slides.append(SlideData(
                title=first_line,
                bullets=["Overview", "Key Topics"]
            ))
            lines = lines[1:]
        
        # Convert each bullet to a slide
        for line in lines:
            # Remove bullet characters
            title = re.sub(r'^[\*\-•]\s*', '', line)
            title = re.sub(r'^\d+\.\s*', '', title)
            
            if title:
                slides.append(SlideData(
                    title=title,
                    bullets=[]  # Will be expanded by content generator
                ))
        
        return slides
    
    async def _parse_nested_outline(self, text: str) -> List[SlideData]:
        """
        Parse a nested outline into slides.
        Top-level items become slide titles, nested items become bullets.
        """
        lines = [l for l in text.split('\n') if l.strip()]
        sections = self._extract_sections(lines)
        
        slides = []
        for section in sections:
            slides.append(SlideData(
                title=section.title,
                bullets=section.sub_points
            ))
        
        return slides
    
    def _extract_sections(self, lines: List[str]) -> List[OutlineSection]:
        """Extract hierarchical sections from outline text."""
        sections = []
        current_section = None
        
        for line in lines:
            indent_level = len(line) - len(line.lstrip())
            clean_line = line.strip()
            
            # Remove bullet/number markers
            clean_line = re.sub(r'^[\*\-•]\s*', '', clean_line)
            clean_line = re.sub(r'^\d+\.\s*', '', clean_line)
            
            if not clean_line:
                continue
            
            # Determine if this is a main section or sub-point
            if indent_level <= 2:  # Main section
                if current_section:
                    sections.append(current_section)
                current_section = OutlineSection(title=clean_line, depth=0)
            else:  # Sub-point
                if current_section:
                    current_section.sub_points.append(clean_line)
        
        # Add last section
        if current_section:
            sections.append(current_section)
        
        return sections
