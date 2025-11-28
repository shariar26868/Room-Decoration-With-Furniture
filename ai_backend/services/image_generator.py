"""
Image Generator Service
=======================
Generate room designs using DALL-E 3
"""

import logging
import requests
import tempfile
from openai import OpenAI
from typing import List
from ai_backend.models import FurnitureItem
from ai_backend.config import OPENAI_API_KEY, DALLE_MODEL, DALLE_SIZE, DALLE_QUALITY

logger = logging.getLogger(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)


def generate_room_design(
    room_image_url: str,
    prompt: str,
    theme: str,
    room_type: str,
    furniture_items: List[FurnitureItem]
) -> str:
    """
    Generate room design using DALL-E 3
    
    Args:
        room_image_url: Original room image URL
        prompt: User's placement instructions
        theme: Design theme
        room_type: Type of room
        furniture_items: Selected furniture items
    
    Returns:
        Path to generated image file
    """
    
    # Build furniture description
    furniture_desc = ", ".join([
        f"{item.name} (${item.price:.0f})"
        for item in furniture_items[:3]  # Limit to 3 for token efficiency
    ])
    
    # Build comprehensive DALL-E prompt
    dalle_prompt = f"""Professional interior design photograph: {theme.replace('_', ' ').title()} style {room_type.lower()}.

DESIGN REQUIREMENTS:
- Style: {theme.replace('_', ' ')}
- Room type: {room_type}
- Furniture to include: {furniture_desc}
- Placement: {prompt}

VISUAL QUALITY:
- Photorealistic, magazine-quality interior
- Natural lighting with soft shadows
- Professional color grading
- Proper scale and perspective
- Comfortable, livable space
- Show furniture clearly and naturally placed

Create a beautiful, functional room that looks like a real home."""

    logger.info(f"🎨 Generating design with DALL-E 3")
    logger.info(f"   Theme: {theme}")
    logger.info(f"   Room: {room_type}")
    logger.info(f"   Furniture: {len(furniture_items)} items")
    
    try:
        # Generate with DALL-E 3
        response = client.images.generate(
            model=DALLE_MODEL,
            prompt=dalle_prompt[:4000],  # DALL-E 3 max: 4000 chars
            size=DALLE_SIZE,
            quality=DALLE_QUALITY,
            n=1
        )
        
        image_url = response.data[0].url
        logger.info(f"✅ DALL-E 3 generated image")
        
        # Download generated image
        img_response = requests.get(image_url, timeout=60)
        img_response.raise_for_status()
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp:
            temp.write(img_response.content)
            temp_path = temp.name
        
        logger.info(f"📥 Downloaded to: {temp_path}")
        
        return temp_path
        
    except Exception as e:
        logger.error(f"❌ DALL-E 3 generation failed: {e}")
        raise Exception(f"Image generation failed: {str(e)}")