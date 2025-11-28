"""
Storage Helper
==============
File storage utility functions
"""

import os
import uuid
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def upload_to_s3(file_path: str, folder: str = "generated") -> str:
    """
    Upload file to S3 with organized folder structure
    
    Args:
        file_path: Local file path
        folder: S3 folder (e.g., 'rooms', 'generated')
    
    Returns:
        Public S3 URL
    """
    from ai_backend.services.aws_service import get_aws_service
    
    # Validate file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Generate unique filename
    file_extension = os.path.splitext(file_path)[1] or ".jpg"
    timestamp = datetime.now().strftime("%Y%m%d")
    unique_id = str(uuid.uuid4())[:8]
    
    # Build S3 key: folder/date/unique_id.ext
    s3_key = f"{folder}/{timestamp}/{unique_id}{file_extension}"
    
    # Upload to S3
    aws_service = get_aws_service()
    url = aws_service.upload_file(file_path, s3_key)
    
    # Cleanup local file
    try:
        os.remove(file_path)
        logger.info(f"🗑️ Cleaned up local file")
    except Exception as e:
        logger.warning(f"⚠️ Could not delete local file: {e}")
    
    return url