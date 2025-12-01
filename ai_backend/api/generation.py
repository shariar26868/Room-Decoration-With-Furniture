"""
Image Generation API
====================
Handle AI image generation with furniture and decorative items
"""

from fastapi import APIRouter, HTTPException, Request
from ai_backend.models import ImageGenerationRequest, ImageGenerationResponse
from ai_backend.services.image_generator import generate_room_design
from ai_backend.services.storage import upload_to_s3
from ai_backend.api.upload import user_sessions
import time
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/generate", response_model=ImageGenerationResponse)
async def generate_image(request: ImageGenerationRequest, req: Request):
    """
    Step 8: Generate final room design image with furniture and optional decorative items
    """
    session = user_sessions.get(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Validate prerequisites
    if not session.search_results:
        raise HTTPException(status_code=400, detail="Please search for furniture first")
    
    # Get selected furniture items
    selected_furniture = [
        item for item in session.search_results
        if item.link in request.furniture_links
    ]
    
    if not selected_furniture:
        raise HTTPException(status_code=400, detail="No valid furniture selected")
    
    # ✅ Get decorative items (optional)
    decorative_items = getattr(session, 'decorative_items', [])
    
    logger.info(f"🎨 Generating design with {len(selected_furniture)} furniture items")
    if decorative_items:
        logger.info(f"   + {len(decorative_items)} decorative items")
    
    start_time = time.time()
    
    try:
        # Generate image with furniture and decorative items
        generated_path = generate_room_design(
            room_image_url=session.room_image_url,
            prompt=request.prompt,
            theme=session.theme,
            room_type=session.room_type,
            furniture_items=selected_furniture,
            decorative_items=decorative_items  # ✅ Pass decorative items
        )
        
        # Upload to S3
        generated_url = upload_to_s3(generated_path, folder="generated")
        
        # Save to session
        session.generated_images.append(generated_url)
        
        generation_time = round(time.time() - start_time, 2)
        
        logger.info(f"✅ Image generated in {generation_time}s")
        
        return ImageGenerationResponse(
            success=True,
            generated_image_url=generated_url,
            original_image_url=session.room_image_url,
            furniture_items=selected_furniture,
            room_type=session.room_type,  # ✅ Added room_type field
            prompt_used=request.prompt,
            generation_time_seconds=generation_time,
            message=f"Room design with {len(selected_furniture)} furniture + {len(decorative_items)} decorative items generated"
        )
        
    except Exception as e:
        logger.error(f"❌ Generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")


@router.get("/history/{session_id}")
async def get_generation_history(session_id: str):
    """Get all generated images for a session"""
    session = user_sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "success": True,
        "session_id": session_id,
        "generated_images": session.generated_images,
        "count": len(session.generated_images)
    }