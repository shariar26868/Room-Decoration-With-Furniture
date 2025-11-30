# # """
# # Selection API
# # =============
# # Handle room type, theme, dimensions, and furniture selection
# # """

# # from fastapi import APIRouter, HTTPException, Request
# # from ai_backend.models import (
# #     RoomTypeRequest, ThemeRequest, RoomDimensionRequest, FurnitureSelectionRequest
# # )
# # from ai_backend.config import THEMES, ROOM_TYPES
# # from ai_backend.services.space_calculator import SpaceCalculator
# # from ai_backend.api.upload import user_sessions
# # import logging

# # router = APIRouter()
# # logger = logging.getLogger(__name__)


# # def get_session(session_id: str):
# #     """Get session or raise error"""
# #     if session_id not in user_sessions:
# #         raise HTTPException(status_code=404, detail="Session not found")
# #     return user_sessions[session_id]


# # # ==================== STEP 2: Room Type ====================
# # @router.get("/options/room-types")
# # async def get_room_types():
# #     """Get available room types"""
# #     return {
# #         "success": True,
# #         "room_types": ROOM_TYPES
# #     }


# # @router.post("/room-type")
# # async def select_room_type(request: RoomTypeRequest):
# #     """Select room type"""
# #     session = get_session(request.session_id)
    
# #     if request.room_type not in ROOM_TYPES:
# #         raise HTTPException(status_code=400, detail=f"Invalid room type")
    
# #     session.room_type = request.room_type
# #     logger.info(f"✅ Room type: {request.room_type}")
    
# #     return {
# #         "success": True,
# #         "room_type": request.room_type,
# #         "message": f"Room type '{request.room_type}' selected"
# #     }


# # # ==================== STEP 3: Theme ====================
# # @router.get("/options/themes")
# # async def get_themes():
# #     """Get available themes"""
# #     return {
# #         "success": True,
# #         "themes": list(THEMES.keys())
# #     }


# # @router.post("/theme")
# # async def select_theme(request: ThemeRequest):
# #     """Select design theme"""
# #     session = get_session(request.session_id)
    
# #     if not session.room_type:
# #         raise HTTPException(status_code=400, detail="Select room type first")
    
# #     theme_upper = request.theme.upper()
# #     if theme_upper not in THEMES:
# #         raise HTTPException(status_code=400, detail="Invalid theme")
    
# #     session.theme = theme_upper
# #     session.theme_websites = THEMES[theme_upper]
    
# #     logger.info(f"✅ Theme: {theme_upper}")
    
# #     return {
# #         "success": True,
# #         "theme": theme_upper,
# #         "websites": session.theme_websites,
# #         "message": f"Theme '{theme_upper}' selected"
# #     }


# # # ==================== STEP 4: Dimensions ====================
# # @router.post("/dimensions")
# # async def set_dimensions(request: RoomDimensionRequest):
# #     """Set room dimensions"""
# #     session = get_session(request.session_id)
    
# #     if not session.room_type or not session.theme:
# #         raise HTTPException(status_code=400, detail="Complete previous steps first")
    
# #     # Calculate areas
# #     session.length = request.length
# #     session.width = request.width
# #     session.height = request.height
# #     session.square_feet = SpaceCalculator.calculate_room_area(request.length, request.width)
# #     session.cubic_feet = SpaceCalculator.calculate_cubic_volume(request.length, request.width, request.height)
    
# #     logger.info(f"✅ Dimensions: {request.length}' x {request.width}' x {request.height}' = {session.square_feet} sqft")
    
# #     return {
# #         "success": True,
# #         "length": request.length,
# #         "width": request.width,
# #         "height": request.height,
# #         "square_feet": round(session.square_feet, 2),
# #         "cubic_feet": round(session.cubic_feet, 2),
# #         "message": f"Room dimensions set: {session.square_feet:.2f} sq ft"
# #     }


# # # ==================== STEP 5: Select Furniture ====================
# # @router.post("/furniture/select")
# # async def select_furniture(req: FurnitureSelectionRequest, request: Request):
# #     """Add furniture to selection with AI space validation"""
# #     session = get_session(req.session_id)
    
# #     if not session.square_feet:
# #         raise HTTPException(status_code=400, detail="Set room dimensions first")
    
# #     # Get product service
# #     product_service = request.app.state.product_service
    
# #     # Get available products for this type
# #     available = product_service.by_type.get(req.furniture_type, [])
# #     if not available:
# #         raise HTTPException(status_code=404, detail=f"No products found for '{req.furniture_type}'")
    
# #     # Use AI to estimate furniture dimensions
# #     logger.info(f"🤖 Estimating dimensions for: {req.subtype}")
# #     dimensions = SpaceCalculator.estimate_furniture_size(
# #         req.furniture_type,
# #         req.subtype,
# #         session.square_feet
# #     )
    
# #     # Validate if furniture fits
# #     validation = SpaceCalculator.validate_furniture_fit(
# #         session.length,
# #         session.width,
# #         session.square_feet,
# #         session.furniture_selections,
# #         dimensions
# #     )
    
# #     if not validation["fits"]:
# #         raise HTTPException(status_code=400, detail=validation["message"])
    
# #     # Add to session
# #     furniture_item = {
# #         "type": req.furniture_type,
# #         "subtype": req.subtype,
# #         "dimensions": dimensions,
# #         "sqft": dimensions["sqft"]
# #     }
    
# #     session.furniture_selections.append(furniture_item)
# #     session.furniture_total_sqft = validation["total_sqft"]
    
# #     logger.info(f"✅ Added: {req.subtype} ({dimensions['sqft']} sqft)")
    
# #     return {
# #         "success": True,
# #         "furniture": furniture_item,
# #         "validation": validation,
# #         "total_items": len(session.furniture_selections),
# #         "message": f"Added {req.subtype}"
# #     }


# # # ==================== GET SESSION ====================
# # @router.get("/session/{session_id}")
# # async def get_session_info(session_id: str):
# #     """Get session data"""
# #     session = get_session(session_id)
    
# #     return {
# #         "success": True,
# #         "session_id": session_id,
# #         "room_type": session.room_type,
# #         "theme": session.theme,
# #         "dimensions": {
# #             "length": session.length,
# #             "width": session.width,
# #             "height": session.height,
# #             "square_feet": session.square_feet
# #         } if session.square_feet else None,
# #         "furniture": {
# #             "items": session.furniture_selections,
# #             "count": len(session.furniture_selections),
# #             "total_sqft": session.furniture_total_sqft
# #         }
# #     }







# """
# Selection API
# =============
# Handle room type, theme, dimensions, and furniture selection
# """

# from fastapi import APIRouter, HTTPException, Request
# from ai_backend.models import (
#     RoomTypeRequest, ThemeRequest, RoomDimensionRequest, FurnitureSelectionRequest
# )
# from ai_backend.config import THEMES, ROOM_TYPES
# from ai_backend.services.space_calculator import SpaceCalculator
# from ai_backend.api.upload import user_sessions
# import logging

# router = APIRouter()
# logger = logging.getLogger(__name__)


# def get_session(session_id: str):
#     """Get session or raise error"""
#     if session_id not in user_sessions:
#         raise HTTPException(status_code=404, detail="Session not found")
#     return user_sessions[session_id]


# def _extract_domain(url: str) -> str:
#     """Helper: Extract domain from URL"""
#     if not url:
#         return ""
#     domain = url.replace("https://", "").replace("http://", "")
#     domain = domain.split("/")[0]
#     domain = domain.replace("www.", "")
#     return domain


# # =================================================================
# # STEP 2: SELECT ROOM TYPE
# # =================================================================
# @router.get("/options/room-types")
# async def get_room_types():
#     """Get available room types"""
#     return {
#         "success": True,
#         "room_types": ROOM_TYPES,
#         "count": len(ROOM_TYPES)
#     }


# @router.post("/room-type")
# async def select_room_type(request: RoomTypeRequest):
#     """Select room type"""
#     session = get_session(request.session_id)
    
#     if request.room_type not in ROOM_TYPES:
#         raise HTTPException(status_code=400, detail=f"Invalid room type. Choose from: {ROOM_TYPES}")
    
#     session.room_type = request.room_type
#     logger.info(f"✅ Room type: {request.room_type}")
    
#     return {
#         "success": True,
#         "room_type": request.room_type,
#         "message": f"Room type '{request.room_type}' selected"
#     }


# # =================================================================
# # STEP 3: SELECT THEME
# # =================================================================
# @router.get("/options/themes")
# async def get_themes():
#     """Get available themes"""
#     options = [
#         {
#             "value": theme,
#             "label": theme.replace('_', ' ').title(),
#             "websites": websites
#         }
#         for theme, websites in THEMES.items()
#     ]
    
#     return {
#         "success": True,
#         "themes": list(THEMES.keys()),
#         "options": options,
#         "count": len(THEMES)
#     }


# @router.post("/theme")
# async def select_theme(request: ThemeRequest):
#     """Select design theme"""
#     session = get_session(request.session_id)
    
#     if not session.room_type:
#         raise HTTPException(status_code=400, detail="Please select room type first")
    
#     theme_upper = request.theme.upper()
#     if theme_upper not in THEMES:
#         raise HTTPException(status_code=400, detail=f"Invalid theme. Choose from: {list(THEMES.keys())}")
    
#     session.theme = theme_upper
#     session.theme_websites = THEMES[theme_upper]
    
#     logger.info(f"✅ Theme: {theme_upper} with {len(session.theme_websites)} websites")
    
#     return {
#         "success": True,
#         "theme": theme_upper,
#         "websites": session.theme_websites,
#         "website_count": len(session.theme_websites),
#         "message": f"Theme '{theme_upper}' selected"
#     }


# # =================================================================
# # STEP 3.5: GET AVAILABLE FURNITURE FROM THEME WEBSITES (NEW!)
# # =================================================================
# @router.get("/available-furniture/{session_id}")
# async def get_available_furniture(session_id: str, request: Request):
#     """
#     Get available furniture types and subtypes from theme websites
#     Call this AFTER theme selection
    
#     Returns furniture catalog grouped by type with all available subtypes
#     """
#     session = get_session(session_id)
    
#     if not session.theme:
#         raise HTTPException(status_code=400, detail="Please select theme first")
    
#     # Get product service
#     product_service = request.app.state.product_service
    
#     # Get theme websites domains
#     theme_domains = [_extract_domain(w) for w in session.theme_websites]
    
#     logger.info(f"🔍 Finding furniture from {len(theme_domains)} theme websites")
    
#     # Find products from theme websites
#     matching_products = []
    
#     for product in product_service.products:
#         product_domain = _extract_domain(product.get("websiteLink", ""))
#         if product_domain in theme_domains:
#             matching_products.append(product)
    
#     logger.info(f"   Found {len(matching_products)} products from theme websites")
    
#     # Group by type and subtype
#     furniture_catalog = {}
    
#     for product in matching_products:
#         prod_type = product.get("type", "Unknown")
#         prod_subtype = product.get("subTypes", "Unknown")
        
#         if prod_type == "Unknown" or prod_subtype == "Unknown":
#             continue
        
#         if prod_type not in furniture_catalog:
#             furniture_catalog[prod_type] = set()
        
#         furniture_catalog[prod_type].add(prod_subtype)
    
#     # Convert sets to sorted lists
#     furniture_catalog = {
#         type_name: sorted(list(subtypes))
#         for type_name, subtypes in sorted(furniture_catalog.items())
#     }
    
#     logger.info(f"✅ Catalog created: {len(furniture_catalog)} furniture types")
    
#     return {
#         "success": True,
#         "session_id": session_id,
#         "theme": session.theme,
#         "furniture_catalog": furniture_catalog,
#         "total_types": len(furniture_catalog),
#         "total_products": len(matching_products),
#         "message": f"Available furniture from {session.theme} theme websites"
#     }


# @router.get("/furniture-subtypes/{session_id}/{furniture_type}")
# async def get_furniture_subtypes_for_type(
#     session_id: str, 
#     furniture_type: str,
#     request: Request
# ):
#     """
#     Get available subtypes for a specific furniture type from theme websites
    
#     Example: /furniture-subtypes/abc123/Sofas
#     Returns: ["2-seater sofa", "3-seater sofa", "Corner sofa"]
#     """
#     session = get_session(session_id)
    
#     if not session.theme:
#         raise HTTPException(status_code=400, detail="Please select theme first")
    
#     # Get product service
#     product_service = request.app.state.product_service
    
#     # Get theme websites domains
#     theme_domains = [_extract_domain(w) for w in session.theme_websites]
    
#     logger.info(f"🔍 Finding subtypes for '{furniture_type}' in {session.theme} theme")
    
#     # Find subtypes for this type from theme websites
#     subtypes = set()
#     product_count = 0
    
#     for product in product_service.products:
#         product_domain = _extract_domain(product.get("websiteLink", ""))
#         prod_type = product.get("type", "")
        
#         # Match theme website and furniture type (case-insensitive)
#         if product_domain in theme_domains and prod_type.lower() == furniture_type.lower():
#             prod_subtype = product.get("subTypes", "")
#             if prod_subtype:
#                 subtypes.add(prod_subtype)
#                 product_count += 1
    
#     subtypes_list = sorted(list(subtypes))
    
#     if not subtypes_list:
#         raise HTTPException(
#             status_code=404, 
#             detail=f"No '{furniture_type}' found in {session.theme} theme websites. Please check available furniture types."
#         )
    
#     logger.info(f"✅ Found {len(subtypes_list)} subtypes for '{furniture_type}' ({product_count} products)")
    
#     return {
#         "success": True,
#         "session_id": session_id,
#         "theme": session.theme,
#         "furniture_type": furniture_type,
#         "subtypes": subtypes_list,
#         "count": len(subtypes_list),
#         "product_count": product_count,
#         "message": f"Found {len(subtypes_list)} subtypes for {furniture_type}"
#     }


# # =================================================================
# # STEP 4: SET ROOM DIMENSIONS
# # =================================================================
# @router.post("/dimensions")
# async def set_dimensions(request: RoomDimensionRequest):
#     """Set room dimensions and calculate area"""
#     session = get_session(request.session_id)
    
#     if not session.room_type or not session.theme:
#         raise HTTPException(status_code=400, detail="Please complete previous steps first (room type and theme)")
    
#     # Calculate areas
#     session.length = request.length
#     session.width = request.width
#     session.height = request.height
#     session.square_feet = SpaceCalculator.calculate_room_area(request.length, request.width)
#     session.cubic_feet = SpaceCalculator.calculate_cubic_volume(request.length, request.width, request.height)
    
#     logger.info(f"✅ Dimensions: {request.length}' × {request.width}' × {request.height}' = {session.square_feet:.2f} sqft")
    
#     return {
#         "success": True,
#         "length": request.length,
#         "width": request.width,
#         "height": request.height,
#         "square_feet": round(session.square_feet, 2),
#         "cubic_feet": round(session.cubic_feet, 2),
#         "message": f"Room dimensions set: {session.square_feet:.2f} sq ft"
#     }


# # =================================================================
# # STEP 5: SELECT FURNITURE WITH AI SPACE VALIDATION
# # =================================================================
# @router.post("/furniture/select")
# async def select_furniture(req: FurnitureSelectionRequest, request: Request):
#     """
#     Add furniture to selection with AI space validation
    
#     AI will:
#     1. Estimate furniture dimensions using GPT-4
#     2. Validate if it fits in the room (max 60% usage)
#     3. Add to selection if valid
#     """
#     session = get_session(req.session_id)
    
#     if not session.square_feet:
#         raise HTTPException(status_code=400, detail="Please set room dimensions first")
    
#     # Get product service
#     product_service = request.app.state.product_service
    
#     # Verify this furniture type exists in database
#     available = product_service.by_type.get(req.furniture_type, [])
#     if not available:
#         # Try to find similar types
#         similar_types = [t for t in product_service.by_type.keys() if req.furniture_type.lower() in t.lower()]
        
#         if similar_types:
#             raise HTTPException(
#                 status_code=404, 
#                 detail=f"Furniture type '{req.furniture_type}' not found. Did you mean: {similar_types}?"
#             )
#         else:
#             raise HTTPException(
#                 status_code=404, 
#                 detail=f"No products found for '{req.furniture_type}'. Use /available-furniture endpoint to see valid types."
#             )
    
#     # Use AI to estimate furniture dimensions
#     logger.info(f"🤖 AI estimating dimensions for: {req.subtype} ({req.furniture_type})")
    
#     try:
#         dimensions = SpaceCalculator.estimate_furniture_size(
#             req.furniture_type,
#             req.subtype,
#             session.square_feet
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Failed to estimate dimensions: {str(e)}"
#         )
    
#     # Validate if furniture fits in room
#     validation = SpaceCalculator.validate_furniture_fit(
#         session.length,
#         session.width,
#         session.square_feet,
#         session.furniture_selections,
#         dimensions
#     )
    
#     if not validation["fits"]:
#         raise HTTPException(status_code=400, detail=validation["message"])
    
#     # Add to session
#     furniture_item = {
#         "type": req.furniture_type,
#         "subtype": req.subtype,
#         "dimensions": dimensions,
#         "sqft": dimensions["sqft"]
#     }
    
#     session.furniture_selections.append(furniture_item)
#     session.furniture_total_sqft = validation["total_sqft"]
    
#     logger.info(f"✅ Added: {req.subtype} ({dimensions['sqft']:.2f} sqft)")
#     logger.info(f"   Room usage: {validation['usage_percent']:.1f}% ({validation['remaining_sqft']:.1f} sqft remaining)")
    
#     return {
#         "success": True,
#         "furniture": furniture_item,
#         "validation": validation,
#         "total_items": len(session.furniture_selections),
#         "message": f"Added {req.subtype}"
#     }


# @router.delete("/furniture/remove/{session_id}/{index}")
# async def remove_furniture(session_id: str, index: int):
#     """Remove furniture item by index"""
#     session = get_session(session_id)
    
#     if index < 0 or index >= len(session.furniture_selections):
#         raise HTTPException(status_code=400, detail=f"Invalid index. Valid range: 0-{len(session.furniture_selections)-1}")
    
#     removed = session.furniture_selections.pop(index)
    
#     # Recalculate total
#     session.furniture_total_sqft = sum(item.get("sqft", 0) for item in session.furniture_selections)
    
#     usage_percent = (session.furniture_total_sqft / session.square_feet) * 100
    
#     logger.info(f"🗑️ Removed: {removed['subtype']} ({removed['sqft']} sqft)")
    
#     return {
#         "success": True,
#         "removed": removed,
#         "remaining_items": len(session.furniture_selections),
#         "total_sqft": round(session.furniture_total_sqft, 2),
#         "usage_percent": round(usage_percent, 2),
#         "message": f"Removed {removed['subtype']}"
#     }


# # =================================================================
# # GET SESSION INFO
# # =================================================================
# @router.get("/session/{session_id}")
# async def get_session_info(session_id: str):
#     """Get complete session data"""
#     session = get_session(session_id)
    
#     return {
#         "success": True,
#         "session_id": session_id,
#         "room_image_url": session.room_image_url,
#         "room_type": session.room_type,
#         "theme": session.theme,
#         "theme_websites": session.theme_websites,
#         "dimensions": {
#             "length": session.length,
#             "width": session.width,
#             "height": session.height,
#             "square_feet": session.square_feet,
#             "cubic_feet": session.cubic_feet
#         } if session.square_feet else None,
#         "furniture": {
#             "items": session.furniture_selections,
#             "count": len(session.furniture_selections),
#             "total_sqft": session.furniture_total_sqft,
#             "usage_percent": round((session.furniture_total_sqft / session.square_feet * 100), 2) if session.square_feet else 0
#         },
#         "price_range": {
#             "min_price": session.min_price,
#             "max_price": session.max_price
#         } if session.min_price is not None else None,
#         "search_results_count": len(session.search_results),
#         "generated_images_count": len(session.generated_images)
#     }






"""
Selection API
=============
Handle room type, theme, dimensions, and furniture selection (single & bulk)
"""

from fastapi import APIRouter, HTTPException, Request
from ai_backend.models import (
    RoomTypeRequest, ThemeRequest, RoomDimensionRequest, 
    FurnitureSelectionRequest, BulkFurnitureSelectionRequest,
    BulkFurnitureSelectionResponse
)
from ai_backend.config import THEMES, ROOM_TYPES
from ai_backend.services.space_calculator import SpaceCalculator
from ai_backend.api.upload import user_sessions
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


def get_session(session_id: str):
    """Get session or raise error"""
    if session_id not in user_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return user_sessions[session_id]


def _extract_domain(url: str) -> str:
    """Helper: Extract domain from URL"""
    if not url:
        return ""
    domain = url.replace("https://", "").replace("http://", "")
    domain = domain.split("/")[0]
    domain = domain.replace("www.", "")
    return domain


# =================================================================
# STEP 2: SELECT ROOM TYPE
# =================================================================
@router.get("/options/room-types")
async def get_room_types():
    """Get available room types"""
    return {
        "success": True,
        "room_types": ROOM_TYPES,
        "count": len(ROOM_TYPES)
    }


@router.post("/room-type")
async def select_room_type(request: RoomTypeRequest):
    """Select room type"""
    session = get_session(request.session_id)
    
    if request.room_type not in ROOM_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid room type. Choose from: {ROOM_TYPES}")
    
    session.room_type = request.room_type
    logger.info(f"✅ Room type: {request.room_type}")
    
    return {
        "success": True,
        "room_type": request.room_type,
        "message": f"Room type '{request.room_type}' selected"
    }


# =================================================================
# STEP 3: SELECT THEME
# =================================================================
@router.get("/options/themes")
async def get_themes():
    """Get available themes"""
    options = [
        {
            "value": theme,
            "label": theme.replace('_', ' ').title(),
            "websites": websites
        }
        for theme, websites in THEMES.items()
    ]
    
    return {
        "success": True,
        "themes": list(THEMES.keys()),
        "options": options,
        "count": len(THEMES)
    }


@router.post("/theme")
async def select_theme(request: ThemeRequest):
    """Select design theme"""
    session = get_session(request.session_id)
    
    if not session.room_type:
        raise HTTPException(status_code=400, detail="Please select room type first")
    
    theme_upper = request.theme.upper()
    if theme_upper not in THEMES:
        raise HTTPException(status_code=400, detail=f"Invalid theme. Choose from: {list(THEMES.keys())}")
    
    session.theme = theme_upper
    session.theme_websites = THEMES[theme_upper]
    
    logger.info(f"✅ Theme: {theme_upper} with {len(session.theme_websites)} websites")
    
    return {
        "success": True,
        "theme": theme_upper,
        "websites": session.theme_websites,
        "website_count": len(session.theme_websites),
        "message": f"Theme '{theme_upper}' selected"
    }


# =================================================================
# STEP 3.5: GET AVAILABLE FURNITURE FROM THEME WEBSITES
# =================================================================
@router.get("/available-furniture/{session_id}")
async def get_available_furniture(session_id: str, request: Request):
    """Get available furniture types and subtypes from theme websites"""
    session = get_session(session_id)
    
    if not session.theme:
        raise HTTPException(status_code=400, detail="Please select theme first")
    
    product_service = request.app.state.product_service
    theme_domains = [_extract_domain(w) for w in session.theme_websites]
    
    logger.info(f"🔍 Finding furniture from {len(theme_domains)} theme websites")
    
    matching_products = []
    for product in product_service.products:
        product_domain = _extract_domain(product.get("websiteLink", ""))
        if product_domain in theme_domains:
            matching_products.append(product)
    
    furniture_catalog = {}
    for product in matching_products:
        prod_type = product.get("type", "Unknown")
        prod_subtype = product.get("subTypes", "Unknown")
        
        if prod_type == "Unknown" or prod_subtype == "Unknown":
            continue
        
        if prod_type not in furniture_catalog:
            furniture_catalog[prod_type] = set()
        
        furniture_catalog[prod_type].add(prod_subtype)
    
    furniture_catalog = {
        type_name: sorted(list(subtypes))
        for type_name, subtypes in sorted(furniture_catalog.items())
    }
    
    logger.info(f"✅ Catalog: {len(furniture_catalog)} types")
    
    return {
        "success": True,
        "session_id": session_id,
        "theme": session.theme,
        "furniture_catalog": furniture_catalog,
        "total_types": len(furniture_catalog),
        "total_products": len(matching_products),
        "message": f"Available furniture from {session.theme} theme"
    }


@router.get("/furniture-subtypes/{session_id}/{furniture_type}")
async def get_furniture_subtypes_for_type(
    session_id: str, 
    furniture_type: str,
    request: Request
):
    """Get subtypes for a specific furniture type"""
    session = get_session(session_id)
    
    if not session.theme:
        raise HTTPException(status_code=400, detail="Select theme first")
    
    product_service = request.app.state.product_service
    theme_domains = [_extract_domain(w) for w in session.theme_websites]
    
    subtypes = set()
    for product in product_service.products:
        product_domain = _extract_domain(product.get("websiteLink", ""))
        prod_type = product.get("type", "")
        
        if product_domain in theme_domains and prod_type.lower() == furniture_type.lower():
            prod_subtype = product.get("subTypes", "")
            if prod_subtype:
                subtypes.add(prod_subtype)
    
    subtypes_list = sorted(list(subtypes))
    
    if not subtypes_list:
        raise HTTPException(status_code=404, detail=f"No '{furniture_type}' found")
    
    return {
        "success": True,
        "furniture_type": furniture_type,
        "subtypes": subtypes_list,
        "count": len(subtypes_list)
    }


# =================================================================
# STEP 4: SET ROOM DIMENSIONS
# =================================================================
@router.post("/dimensions")
async def set_dimensions(request: RoomDimensionRequest):
    """Set room dimensions"""
    session = get_session(request.session_id)
    
    if not session.room_type or not session.theme:
        raise HTTPException(status_code=400, detail="Complete previous steps first")
    
    session.length = request.length
    session.width = request.width
    session.height = request.height
    session.square_feet = SpaceCalculator.calculate_room_area(request.length, request.width)
    session.cubic_feet = SpaceCalculator.calculate_cubic_volume(request.length, request.width, request.height)
    
    logger.info(f"✅ Dimensions: {request.length}' × {request.width}' × {request.height}' = {session.square_feet:.2f} sqft")
    
    return {
        "success": True,
        "length": request.length,
        "width": request.width,
        "height": request.height,
        "square_feet": round(session.square_feet, 2),
        "cubic_feet": round(session.cubic_feet, 2),
        "message": f"Room: {session.square_feet:.2f} sq ft"
    }


# =================================================================
# STEP 5: SELECT FURNITURE (SINGLE)
# =================================================================
@router.post("/furniture/select")
async def select_furniture(req: FurnitureSelectionRequest, request: Request):
    """Add single furniture item with AI validation"""
    session = get_session(req.session_id)
    
    if not session.square_feet:
        raise HTTPException(status_code=400, detail="Set room dimensions first")
    
    product_service = request.app.state.product_service
    
    available = product_service.by_type.get(req.furniture_type, [])
    if not available:
        raise HTTPException(status_code=404, detail=f"Type '{req.furniture_type}' not found")
    
    logger.info(f"🤖 Estimating: {req.subtype} ({req.furniture_type})")
    
    dimensions = SpaceCalculator.estimate_furniture_size(
        req.furniture_type,
        req.subtype,
        session.square_feet
    )
    
    validation = SpaceCalculator.validate_furniture_fit(
        session.length,
        session.width,
        session.square_feet,
        session.furniture_selections,
        dimensions
    )
    
    if not validation["fits"]:
        raise HTTPException(status_code=400, detail=validation["message"])
    
    furniture_item = {
        "type": req.furniture_type,
        "subtype": req.subtype,
        "dimensions": dimensions,
        "sqft": dimensions["sqft"]
    }
    
    session.furniture_selections.append(furniture_item)
    session.furniture_total_sqft = validation["total_sqft"]
    
    logger.info(f"✅ Added: {req.subtype} ({dimensions['sqft']:.2f} sqft)")
    
    return {
        "success": True,
        "furniture": furniture_item,
        "validation": validation,
        "total_items": len(session.furniture_selections),
        "message": f"Added {req.subtype}"
    }


# =================================================================
# ✅ NEW: BULK FURNITURE SELECTION
# =================================================================
@router.post("/furniture/select-bulk", response_model=BulkFurnitureSelectionResponse)
async def select_furniture_bulk(req: BulkFurnitureSelectionRequest, request: Request):
    """Add multiple furniture items at once with AI validation"""
    session = get_session(req.session_id)
    
    if not session.square_feet:
        raise HTTPException(status_code=400, detail="Set room dimensions first")
    
    product_service = request.app.state.product_service
    
    logger.info(f"🪑 Bulk selection: {len(req.furniture_items)} items")
    
    added_items = []
    failed_items = []
    temp_selections = []
    
    # Validate and estimate all items
    for idx, item in enumerate(req.furniture_items, 1):
        logger.info(f"\n📦 Item {idx}/{len(req.furniture_items)}: {item.subtype}")
        
        try:
            available = product_service.by_type.get(item.furniture_type, [])
            if not available:
                failed_items.append({
                    "furniture_type": item.furniture_type,
                    "subtype": item.subtype,
                    "error": f"Type '{item.furniture_type}' not found"
                })
                continue
            
            dimensions = SpaceCalculator.estimate_furniture_size(
                item.furniture_type,
                item.subtype,
                session.square_feet
            )
            
            furniture_item = {
                "type": item.furniture_type,
                "subtype": item.subtype,
                "dimensions": dimensions,
                "sqft": dimensions["sqft"]
            }
            
            temp_selections.append(furniture_item)
            logger.info(f"   ✅ {dimensions['sqft']:.2f} sqft")
            
        except Exception as e:
            failed_items.append({
                "furniture_type": item.furniture_type,
                "subtype": item.subtype,
                "error": str(e)
            })
            logger.error(f"   ❌ {e}")
    
    # Validate total space
    if temp_selections:
        total_new_sqft = sum(item["sqft"] for item in temp_selections)
        current_sqft = session.furniture_total_sqft
        combined_total = current_sqft + total_new_sqft
        
        room_sqft = session.square_feet
        usage_percent = (combined_total / room_sqft) * 100
        remaining_sqft = room_sqft - combined_total
        
        from ai_backend.config import MAX_ROOM_USAGE_PERCENT
        
        logger.info(f"\n📊 Space: {combined_total:.2f} sqft ({usage_percent:.1f}%)")
        
        if usage_percent > MAX_ROOM_USAGE_PERCENT:
            raise HTTPException(
                status_code=400,
                detail=f"Room too crowded! Usage: {usage_percent:.1f}% (max: {MAX_ROOM_USAGE_PERCENT}%)"
            )
        
        # Add all items
        for item in temp_selections:
            session.furniture_selections.append(item)
            added_items.append(item)
        
        session.furniture_total_sqft = combined_total
        
        logger.info(f"✅ Added {len(added_items)} items, {len(failed_items)} failed")
        
        return BulkFurnitureSelectionResponse(
            success=True,
            added_items=added_items,
            failed_items=failed_items,
            total_added=len(added_items),
            total_failed=len(failed_items),
            room_usage_percent=round(usage_percent, 2),
            remaining_sqft=round(remaining_sqft, 2),
            message=f"Added {len(added_items)} items. Usage: {usage_percent:.1f}%"
        )
    
    raise HTTPException(status_code=400, detail=f"No items added. {len(failed_items)} failed")


@router.delete("/furniture/remove/{session_id}/{index}")
async def remove_furniture(session_id: str, index: int):
    """Remove furniture by index"""
    session = get_session(session_id)
    
    if index < 0 or index >= len(session.furniture_selections):
        raise HTTPException(status_code=400, detail=f"Invalid index")
    
    removed = session.furniture_selections.pop(index)
    session.furniture_total_sqft = sum(item.get("sqft", 0) for item in session.furniture_selections)
    
    logger.info(f"🗑️ Removed: {removed['subtype']}")
    
    return {
        "success": True,
        "removed": removed,
        "remaining_items": len(session.furniture_selections),
        "message": f"Removed {removed['subtype']}"
    }


@router.delete("/furniture/clear/{session_id}")
async def clear_all_furniture(session_id: str):
    """Clear all furniture"""
    session = get_session(session_id)
    
    count = len(session.furniture_selections)
    session.furniture_selections = []
    session.furniture_total_sqft = 0.0
    
    logger.info(f"🗑️ Cleared {count} items")
    
    return {
        "success": True,
        "cleared_count": count,
        "message": f"Cleared {count} items"
    }


@router.get("/furniture/list/{session_id}")
async def list_selected_furniture(session_id: str):
    """List all selected furniture"""
    session = get_session(session_id)
    
    usage_percent = 0
    if session.square_feet and session.square_feet > 0:
        usage_percent = (session.furniture_total_sqft / session.square_feet) * 100
    
    return {
        "success": True,
        "furniture_items": session.furniture_selections,
        "count": len(session.furniture_selections),
        "total_sqft": round(session.furniture_total_sqft, 2),
        "room_sqft": session.square_feet,
        "usage_percent": round(usage_percent, 2),
        "remaining_sqft": round(session.square_feet - session.furniture_total_sqft, 2) if session.square_feet else 0,
        "message": f"{len(session.furniture_selections)} items selected"
    }


# =================================================================
# GET SESSION INFO
# =================================================================
@router.get("/session/{session_id}")
async def get_session_info(session_id: str):
    """Get complete session data"""
    session = get_session(session_id)
    
    return {
        "success": True,
        "session_id": session_id,
        "room_image_url": session.room_image_url,
        "room_type": session.room_type,
        "theme": session.theme,
        "dimensions": {
            "length": session.length,
            "width": session.width,
            "height": session.height,
            "square_feet": session.square_feet
        } if session.square_feet else None,
        "furniture": {
            "items": session.furniture_selections,
            "count": len(session.furniture_selections),
            "total_sqft": session.furniture_total_sqft,
            "usage_percent": round((session.furniture_total_sqft / session.square_feet * 100), 2) if session.square_feet else 0
        },
        "price_range": {
            "min_price": session.min_price,
            "max_price": session.max_price
        } if session.min_price is not None else None,
        "search_results_count": len(session.search_results),
        "generated_images_count": len(session.generated_images)
    }