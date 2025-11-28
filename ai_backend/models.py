"""
Pydantic Models
===============
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# ==================== SESSION ====================
class UserSession:
    """User session storage"""
    def __init__(self, session_id: str, room_image_url: str):
        self.session_id = session_id
        self.room_image_url = room_image_url
        self.room_type: Optional[str] = None
        self.theme: Optional[str] = None
        self.theme_websites: List[str] = []
        self.length: Optional[float] = None
        self.width: Optional[float] = None
        self.height: Optional[float] = None
        self.square_feet: Optional[float] = None
        self.cubic_feet: Optional[float] = None
        self.furniture_selections: List[Dict] = []
        self.furniture_total_sqft: float = 0.0
        self.min_price: Optional[float] = None
        self.max_price: Optional[float] = None
        self.search_results: List[Any] = []
        self.generated_images: List[str] = []


# ==================== REQUESTS ====================
class RoomImageUploadResponse(BaseModel):
    success: bool
    image_url: str
    session_id: str
    message: str


class RoomTypeRequest(BaseModel):
    session_id: str
    room_type: str


class ThemeRequest(BaseModel):
    session_id: str
    theme: str


class RoomDimensionRequest(BaseModel):
    session_id: str
    length: float = Field(..., gt=0, description="Length in feet")
    width: float = Field(..., gt=0, description="Width in feet")
    height: float = Field(..., gt=0, description="Height in feet")


class FurnitureSelectionRequest(BaseModel):
    session_id: str
    furniture_type: str
    subtype: str


class PriceRangeRequest(BaseModel):
    session_id: str
    min_price: float = Field(..., ge=0)
    max_price: float = Field(..., gt=0)


class FurnitureSearchRequest(BaseModel):
    session_id: str


class ImageGenerationRequest(BaseModel):
    session_id: str
    furniture_links: List[str]
    prompt: str = "Place furniture naturally in the room"


# ==================== RESPONSES ====================
class FurnitureItem(BaseModel):
    name: str
    link: str
    price: float
    image_url: str
    website: str
    type: str
    subtype: str


class ImageGenerationResponse(BaseModel):
    success: bool
    generated_image_url: str
    original_image_url: str
    furniture_items: List[FurnitureItem]
    prompt_used: str
    generation_time_seconds: float
    message: str