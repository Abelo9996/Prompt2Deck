"""
Simple test script to verify the Prompt2Deck backend is working.
Run this after setting up the environment to test the pipeline.
"""

import asyncio
from pipeline.outline_parser import OutlineParser
from pipeline.content_generator import ContentGenerator
from pipeline.slide_builder import SlideBuilder


async def test_pipeline():
    """Test the full pipeline with a simple example."""
    print("🧪 Testing Prompt2Deck Pipeline...\n")
    
    # Test input
    test_input = """
    Introduction to Machine Learning
    
    * What is Machine Learning?
    * Types of Machine Learning
    * Applications
    * Getting Started
    """
    
    # Step 1: Parse outline
    print("1️⃣ Parsing outline...")
    parser = OutlineParser()
    slides = await parser.parse(test_input)
    print(f"   ✅ Created {len(slides)} slides\n")
    
    # Step 2: Expand content
    print("2️⃣ Expanding content...")
    generator = ContentGenerator()
    expanded_slides = await generator.expand_slides(slides, include_speaker_notes=True)
    print(f"   ✅ Expanded content for {len(expanded_slides)} slides\n")
    
    # Display first slide
    if expanded_slides:
        first_slide = expanded_slides[0]
        print("📄 First Slide Preview:")
        print(f"   Title: {first_slide.title}")
        print(f"   Bullets: {len(first_slide.bullets)}")
        if first_slide.speaker_notes:
            print(f"   Notes: {first_slide.speaker_notes[:80]}...")
        print()
    
    # Step 3: Build deck
    print("3️⃣ Building PowerPoint deck...")
    builder = SlideBuilder()
    output_path = await builder.build_deck(
        expanded_slides,
        output_dir="output",
        theme="professional"
    )
    print(f"   ✅ Deck created at: {output_path}\n")
    
    print("✨ Pipeline test complete!")
    print(f"📊 Generated {len(expanded_slides)} slides")
    print(f"📁 Output: {output_path}")


if __name__ == "__main__":
    asyncio.run(test_pipeline())
