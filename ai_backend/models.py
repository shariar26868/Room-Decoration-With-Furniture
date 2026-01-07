# """
# Pydantic Models
# ===============
# """

# from pydantic import BaseModel, Field
# from typing import List, Optional, Dict, Any

# # ==================== SESSION ====================
# class UserSession:
#     """User session storage"""
#     def __init__(self, session_id: str, room_image_url: str):
#         self.session_id = session_id
#         self.room_image_url = room_image_url
#         self.room_type: Optional[str] = None
#         self.theme: Optional[str] = None
#         self.theme_websites: List[str] = []
#         self.length: Optional[float] = None
#         self.width: Optional[float] = None
#         self.height: Optional[float] = None
#         self.square_feet: Optional[float] = None
#         self.cubic_feet: Optional[float] = None
#         self.furniture_selections: List[Dict] = []
#         self.furniture_total_sqft: float = 0.0
#         self.min_price: Optional[float] = None
#         self.max_price: Optional[float] = None
#         self.search_results: List[Any] = []
#         self.generated_images: List[str] = []
#         self.decorative_items: List[Dict] = []


# # ==================== REQUESTS ====================
# class RoomImageUploadResponse(BaseModel):
#     success: bool
#     image_url: str
#     session_id: str
#     message: str


# class RoomTypeRequest(BaseModel):
#     session_id: str
#     room_type: str


# class ThemeRequest(BaseModel):
#     session_id: str
#     theme: str


# class RoomDimensionRequest(BaseModel):
#     session_id: str
#     length: float = Field(..., gt=0, description="Length in feet")
#     width: float = Field(..., gt=0, description="Width in feet")
#     height: float = Field(..., gt=0, description="Height in feet")


# class FurnitureSelectionRequest(BaseModel):
#     session_id: str
#     furniture_type: str
#     subtype: str


# class PriceRangeRequest(BaseModel):
#     session_id: str
#     min_price: float = Field(..., ge=0)
#     max_price: float = Field(..., gt=0)


# class FurnitureSearchRequest(BaseModel):
#     session_id: str


# class ImageGenerationRequest(BaseModel):
#     session_id: str
#     furniture_links: List[str]
#     prompt: str = "Place furniture naturally in the room"


# # ==================== RESPONSES ====================
# class FurnitureItem(BaseModel):
#     name: str
#     link: str
#     price: float
#     image_url: str
#     website: str
#     type: str
#     subtype: str


# class ImageGenerationResponse(BaseModel):
#     success: bool
#     generated_image_url: str
#     original_image_url: str
#     furniture_items: List[FurnitureItem]
#     room_type: str  # ✅ Added room_type field
#     prompt_used: str
#     generation_time_seconds: float
#     message: str


# # ==================== DECORATIVE ITEMS ====================
# class DecorativeItemUpload(BaseModel):
#     """Upload custom decorative item"""
#     session_id: str
#     item_name: str = Field(..., description="Name of item (e.g., 'Wall Clock', 'Lamp', 'Painting')")
#     placement_hint: Optional[str] = Field(None, description="Where to place (e.g., 'on wall', 'on table', 'corner')")


# class DecorativeItemResponse(BaseModel):
#     """Response after uploading decorative item"""
#     success: bool
#     item_id: str
#     item_name: str
#     image_url: str
#     placement_hint: Optional[str]
#     message: str


# class DecorativeItemsList(BaseModel):
#     """List of decorative items"""
#     success: bool
#     session_id: str
#     items: List[Dict]
#     count: int
#     message: str


# class RemoveDecorativeItemRequest(BaseModel):
#     """Remove a decorative item"""
#     session_id: str
#     item_id: str


# # ==================== BULK FURNITURE SELECTION ====================
# class BulkFurnitureItem(BaseModel):
#     """Single furniture item for bulk selection"""
#     furniture_type: str
#     subtype: str


# class BulkFurnitureSelectionRequest(BaseModel):
#     """Select multiple furniture items at once"""
#     session_id: str
#     furniture_items: List[BulkFurnitureItem] = Field(..., description="List of furniture to add")


# class BulkFurnitureSelectionResponse(BaseModel):
#     """Response after bulk selection"""
#     success: bool
#     added_items: List[dict]
#     failed_items: List[dict]
#     total_added: int
#     total_failed: int
#     room_usage_percent: float
#     remaining_sqft: float
#     message: str




# """
# Pydantic Models
# ===============
# """

# from pydantic import BaseModel, Field
# from typing import List, Optional, Dict, Any

# # ==================== SESSION ====================
# class UserSession:
#     """User session storage"""
#     def __init__(self, session_id: str, room_image_url: str):
#         self.session_id = session_id
#         self.room_image_url = room_image_url
#         self.room_type: Optional[str] = None
#         self.theme: Optional[str] = None
#         self.theme_websites: List[str] = []
#         self.length: Optional[float] = None
#         self.width: Optional[float] = None
#         self.height: Optional[float] = None
#         self.square_inches: Optional[float] = None
#         self.cubic_inches: Optional[float] = None
#         self.furniture_selections: List[Dict] = []
#         self.furniture_total_sqin: float = 0.0
#         self.min_price: Optional[float] = None
#         self.max_price: Optional[float] = None
#         self.search_results: List[Any] = []
#         self.generated_images: List[str] = []
#         self.decorative_items: List[Dict] = []


# # ==================== REQUESTS ====================
# class RoomImageUploadResponse(BaseModel):
#     success: bool
#     image_url: str
#     session_id: str
#     message: str


# class RoomTypeRequest(BaseModel):
#     session_id: str
#     room_type: str


# class ThemeRequest(BaseModel):
#     session_id: str
#     theme: str


# class RoomDimensionRequest(BaseModel):
#     session_id: str
#     length: float = Field(..., gt=0, description="Length in inches")
#     width: float = Field(..., gt=0, description="Width in inches")
#     height: float = Field(..., gt=0, description="Height in inches")


# class FurnitureSelectionRequest(BaseModel):
#     session_id: str
#     furniture_type: str
#     subtype: str


# class PriceRangeRequest(BaseModel):
#     session_id: str
#     min_price: float = Field(..., ge=0)
#     max_price: float = Field(..., gt=0)


# class FurnitureSearchRequest(BaseModel):
#     session_id: str


# class ImageGenerationRequest(BaseModel):
#     session_id: str
#     furniture_links: List[str]
#     prompt: str = "Place furniture naturally in the room"


# # ==================== RESPONSES ====================
# class FurnitureItem(BaseModel):
#     name: str
#     link: str
#     price: float
#     image_url: str
#     website: str
#     type: str
#     subtype: str


# class ImageGenerationResponse(BaseModel):
#     success: bool
#     generated_image_url: str
#     original_image_url: str
#     furniture_items: List[FurnitureItem]
#     room_type: str
#     prompt_used: str
#     generation_time_seconds: float
#     message: str


# # ==================== DECORATIVE ITEMS ====================
# class DecorativeItemUpload(BaseModel):
#     """Upload custom decorative item"""
#     session_id: str
#     item_name: str = Field(..., description="Name of item (e.g., 'Wall Clock', 'Lamp', 'Painting')")
#     placement_hint: Optional[str] = Field(None, description="Where to place (e.g., 'on wall', 'on table', 'corner')")


# class DecorativeItemResponse(BaseModel):
#     """Response after uploading decorative item"""
#     success: bool
#     item_id: str
#     item_name: str
#     image_url: str
#     placement_hint: Optional[str]
#     message: str


# class DecorativeItemsList(BaseModel):
#     """List of decorative items"""
#     success: bool
#     session_id: str
#     items: List[Dict]
#     count: int
#     message: str


# class RemoveDecorativeItemRequest(BaseModel):
#     """Remove a decorative item"""
#     session_id: str
#     item_id: str


# # ==================== BULK FURNITURE SELECTION ====================
# class BulkFurnitureItem(BaseModel):
#     """Single furniture item for bulk selection"""
#     furniture_type: str
#     subtype: str


# class BulkFurnitureSelectionRequest(BaseModel):
#     """Select multiple furniture items at once"""
#     session_id: str
#     furniture_items: List[BulkFurnitureItem] = Field(..., description="List of furniture to add")


# class BulkFurnitureSelectionResponse(BaseModel):
#     """Response after bulk selection"""
#     success: bool
#     added_items: List[dict]
#     failed_items: List[dict]
#     total_added: int
#     total_failed: int
#     room_usage_percent: float
#     remaining_sqin: float
#     message: str











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
        self.length: Optional[float] = None  # in cm
        self.width: Optional[float] = None   # in cm
        self.height: Optional[float] = None  # in cm
        self.square_feet: Optional[float] = None  # Actually sq cm (keeping name for compatibility)
        self.cubic_feet: Optional[float] = None   # Actually cubic cm (keeping name for compatibility)
        self.furniture_selections: List[Dict] = []
        self.furniture_total_sqft: float = 0.0    # Actually sq cm (keeping name for compatibility)
        self.min_price: Optional[float] = None
        self.max_price: Optional[float] = None
        self.search_results: List[Any] = []
        self.generated_images: List[str] = []
        self.decorative_items: List[Dict] = []


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
    length: float = Field(..., gt=0, description="Length in centimeters")
    width: float = Field(..., gt=0, description="Width in centimeters")
    height: float = Field(..., gt=0, description="Height in centimeters")


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
    room_type: str
    prompt_used: str
    generation_time_seconds: float
    message: str


# ==================== DECORATIVE ITEMS ====================
class DecorativeItemUpload(BaseModel):
    """Upload custom decorative item"""
    session_id: str
    item_name: str = Field(..., description="Name of item (e.g., 'Wall Clock', 'Lamp', 'Painting')")
    placement_hint: Optional[str] = Field(None, description="Where to place (e.g., 'on wall', 'on table', 'corner')")


class DecorativeItemResponse(BaseModel):
    """Response after uploading decorative item"""
    success: bool
    item_id: str
    item_name: str
    image_url: str
    placement_hint: Optional[str]
    message: str


class DecorativeItemsList(BaseModel):
    """List of decorative items"""
    success: bool
    session_id: str
    items: List[Dict]
    count: int
    message: str


class RemoveDecorativeItemRequest(BaseModel):
    """Remove a decorative item"""
    session_id: str
    item_id: str


# ==================== BULK FURNITURE SELECTION ====================
class BulkFurnitureItem(BaseModel):
    """Single furniture item for bulk selection"""
    furniture_type: str
    subtype: str


class BulkFurnitureSelectionRequest(BaseModel):
    """Select multiple furniture items at once"""
    session_id: str
    furniture_items: List[BulkFurnitureItem] = Field(..., description="List of furniture to add")


class BulkFurnitureSelectionResponse(BaseModel):
    """Response after bulk selection"""
    success: bool
    added_items: List[dict]
    failed_items: List[dict]
    total_added: int
    total_failed: int
    room_usage_percent: float
    remaining_sqcm: float  # ✅ Changed from remaining_sqin
    message: str