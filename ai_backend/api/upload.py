"""
Upload API
==========
Handle room image upload
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from ai_backend.services.storage import upload_to_s3
from ai_backend.models import RoomImageUploadResponse, UserSession
import uuid
import tempfile
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# In-memory session storage
user_sessions = {}


@router.post("/upload", response_model=RoomImageUploadResponse)
async def upload_room_image(room_image: UploadFile = File(...)):
    """
    Step 1: Upload room image
    """
    try:
        logger.info(f"📤 Uploading image: {room_image.filename}")
        
        # Read image
        image_bytes = await room_image.read()
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp:
            temp.write(image_bytes)
            temp_path = temp.name
        
        # Upload to S3
        s3_url = upload_to_s3(temp_path, folder="rooms")
        
        # Create session
        session_id = str(uuid.uuid4())
        user_sessions[session_id] = UserSession(
            session_id=session_id,
            room_image_url=s3_url
        )
        
        logger.info(f"✅ Image uploaded: {session_id}")
        
        return RoomImageUploadResponse(
            success=True,
            image_url=s3_url,
            session_id=session_id,
            message="Room image uploaded successfully"
        )
        
    except Exception as e:
        logger.error(f"❌ Upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))