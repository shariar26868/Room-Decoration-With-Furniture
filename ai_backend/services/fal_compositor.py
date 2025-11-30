"""
FAL.ai SeeDream Compositor
==========================
Uses FAL.ai SeeDream API for intelligent furniture placement
"""

import logging
import os
import requests
import tempfile
import base64
import io
from PIL import Image
from typing import List
import fal_client
from ai_backend.models import FurnitureItem
from ai_backend.config import FAL_API_KEY

logger = logging.getLogger(__name__)


class FALCompositor:
    """AI-powered furniture composition using FAL.ai SeeDream"""
    
    def __init__(self):
        if not FAL_API_KEY:
            raise ValueError("FAL_API_KEY is required in .env file")
        
        # Configure FAL client
        os.environ["FAL_KEY"] = FAL_API_KEY
        fal_client.api_key = FAL_API_KEY
        
        logger.info("✅ FAL.ai SeeDream compositor initialized")
    
    def compose_furniture_in_room(
        self,
        room_image_url: str,
        furniture_items: List[FurnitureItem],
        placement_prompt: str,
        room_type: str,
        theme: str
    ) -> str:
        """
        Compose furniture into room using FAL.ai SeeDream
        
        Args:
            room_image_url: URL of the room image
            furniture_items: List of furniture to place
            placement_prompt: User's placement instructions
            room_type: Type of room
            theme: Design theme
        
        Returns:
            Path to generated image file
        """
        
        logger.info(f"🎨 FAL.ai composing {len(furniture_items)} furniture items")
        logger.info(f"   Theme: {theme}")
        logger.info(f"   Room: {room_type}")
        logger.info(f"   Placement: {placement_prompt}")
        
        try:
            # Step 1: Download room image
            room_image_base64 = self._download_and_encode_image(room_image_url)
            
            # Step 2: Download all furniture images
            furniture_images = []
            for idx, item in enumerate(furniture_items, 1):
                logger.info(f"   📥 [{idx}] {item.name} - ${item.price:.0f}")
                furniture_base64 = self._download_and_encode_image(item.image_url)
                furniture_images.append(furniture_base64)
            
            # Step 3: Create comprehensive prompt for FAL.ai
            ai_prompt = self._create_composition_prompt(
                furniture_items,
                placement_prompt,
                room_type,
                theme
            )
            
            logger.info(f"🤖 AI Prompt: {ai_prompt[:150]}...")
            
            # Step 4: Combine images (room + all furniture)
            all_images = [room_image_base64] + furniture_images
            
            # Step 5: Call FAL.ai SeeDream API
            logger.info(f"🚀 Calling FAL.ai SeeDream with {len(all_images)} images...")
            
            handler = fal_client.submit(
                "fal-ai/bytedance/seedream/v4/edit",
                arguments={
                    "prompt": ai_prompt,
                    "image_urls": all_images,
                    "aspect_ratio": "landscape",  # Room images are usually landscape
                    "num_inference_steps": 50,
                    "guidance_scale": 7.5,
                    "num_images": 1
                }
            )
            
            # Get result
            result = handler.get()
            
            if not result or "images" not in result or not result["images"]:
                raise Exception("FAL.ai did not return any images")
            
            # Step 6: Download generated image
            generated_url = result["images"][0]["url"]
            logger.info(f"✅ FAL.ai generated image: {generated_url[:50]}...")
            
            # Save to temp file
            output_path = self._download_result_image(generated_url)
            
            logger.info(f"💾 Saved: {output_path}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"❌ FAL.ai composition failed: {e}")
            raise Exception(f"AI composition failed: {str(e)}")
    
    def _download_and_encode_image(self, image_url: str) -> str:
        """Download image from URL and encode to base64 data URL"""
        try:
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            image_bytes = response.content
            
            # Resize if too large (FAL.ai limit: 4000x4000)
            image = Image.open(io.BytesIO(image_bytes))
            
            if image.width > 4000 or image.height > 4000:
                logger.info(f"   Resizing image from {image.size}")
                
                # Calculate new size maintaining aspect ratio
                max_dim = 4000
                if image.width > image.height:
                    new_width = max_dim
                    new_height = int((image.height * max_dim) / image.width)
                else:
                    new_height = max_dim
                    new_width = int((image.width * max_dim) / image.height)
                
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Convert back to bytes
                output = io.BytesIO()
                image.save(output, format='JPEG', quality=95)
                image_bytes = output.getvalue()
            
            # Encode to base64
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            
            # Determine content type
            content_type = "image/jpeg"
            if image_url.endswith('.png'):
                content_type = "image/png"
            
            data_url = f"data:{content_type};base64,{image_base64}"
            
            return data_url
            
        except Exception as e:
            logger.error(f"Failed to download/encode image: {e}")
            raise
    
    def _create_composition_prompt(
        self,
        furniture_items: List[FurnitureItem],
        placement_prompt: str,
        room_type: str,
        theme: str
    ) -> str:
        """Create detailed prompt for AI composition"""
        
        # List furniture items
        furniture_list = ", ".join([
            f"{item.name} (${item.price:.0f})"
            for item in furniture_items
        ])
        
        prompt = f"""Professional interior design: Place the following furniture naturally in this {room_type.lower()} with {theme.lower()} style.

Furniture to place: {furniture_list}

User instructions: {placement_prompt}

Requirements:
- Place furniture realistically on the floor, not floating
- Maintain proper perspective and scale
- Follow {theme.lower()} design principles
- Ensure furniture fits naturally in the space
- Keep realistic shadows and lighting
- Blend furniture seamlessly with the room

Create a photorealistic, professionally designed interior."""
        
        return prompt
    
    def _download_result_image(self, image_url: str) -> str:
        """Download final generated image and save to temp file"""
        try:
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # Save to temp file
            output_path = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to download result: {e}")
            raise


# Create singleton instance
fal_compositor = FALCompositor()