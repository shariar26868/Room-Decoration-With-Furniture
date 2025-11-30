"""
Image Generator Service
=======================
Generate room designs using FAL.ai SeeDream
"""

import logging
from typing import List
from ai_backend.models import FurnitureItem
from ai_backend.services.fal_compositor import fal_compositor

logger = logging.getLogger(__name__)


def generate_room_design(
    room_image_url: str,
    prompt: str,
    theme: str,
    room_type: str,
    furniture_items: List[FurnitureItem],
    decorative_items: list = None
) -> str:
    """
    Generate room design using FAL.ai SeeDream
    
    Args:
        room_image_url: Original room image URL
        prompt: User's placement instructions
        theme: Design theme
        room_type: Type of room
        furniture_items: Selected furniture items
        decorative_items: Optional decorative items (not used with FAL.ai)
    
    Returns:
        Path to generated image file
    """
    
    logger.info(f"🎨 Generating design with {len(furniture_items)} furniture items")
    logger.info(f"   Theme: {theme}")
    logger.info(f"   Room: {room_type}")
    logger.info(f"   Placement: {prompt}")
    
    # Log furniture items
    for idx, item in enumerate(furniture_items, 1):
        logger.info(f"   {idx}. {item.name} - ${item.price:.0f} from {item.website}")
    
    try:
        # Use FAL.ai compositor
        generated_path = fal_compositor.compose_furniture_in_room(
            room_image_url=room_image_url,
            furniture_items=furniture_items,
            placement_prompt=prompt,
            room_type=room_type,
            theme=theme
        )
        
        logger.info(f"✅ Room design generated successfully with FAL.ai")
        
        return generated_path
        
    except Exception as e:
        logger.error(f"❌ Room design generation failed: {e}")
        raise Exception(f"Image generation failed: {str(e)}")