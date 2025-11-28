"""
Furniture API
=============
Handle price range and product search
"""

from fastapi import APIRouter, HTTPException, Request
from ai_backend.models import PriceRangeRequest, FurnitureSearchRequest, FurnitureItem
from ai_backend.services.furniture_search import search_furniture_from_database
from ai_backend.api.upload import user_sessions
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


# ==================== STEP 6: Price Range ====================
@router.post("/price-range")
async def set_price_range(request: PriceRangeRequest):
    """Set price range for furniture search"""
    session = user_sessions.get(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if request.min_price > request.max_price:
        raise HTTPException(status_code=400, detail="min_price cannot be greater than max_price")
    
    session.min_price = request.min_price
    session.max_price = request.max_price
    
    logger.info(f"💰 Price range: ${request.min_price} - ${request.max_price}")
    
    return {
        "success": True,
        "min_price": request.min_price,
        "max_price": request.max_price,
        "message": f"Price range set: ${request.min_price} - ${request.max_price}"
    }


# ==================== STEP 7: Search Furniture ====================
@router.post("/search")
async def search_furniture(request: FurnitureSearchRequest, req: Request):
    """Search for furniture products from database"""
    session = user_sessions.get(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Validate prerequisites
    if not session.furniture_selections:
        raise HTTPException(status_code=400, detail="Please select furniture first")
    
    if session.min_price is None or session.max_price is None:
        raise HTTPException(status_code=400, detail="Please set price range first")
    
    # Get product service
    product_service = req.app.state.product_service
    
    # Search for each furniture item
    logger.info(f"🔍 Searching for {len(session.furniture_selections)} furniture items")
    
    results = search_furniture_from_database(
        product_service=product_service,
        furniture_selections=session.furniture_selections,
        theme_websites=session.theme_websites,
        min_price=session.min_price,
        max_price=session.max_price
    )
    
    session.search_results = results
    
    logger.info(f"✅ Found {len(results)} products")
    
    return {
        "success": True,
        "results": [item.dict() for item in results],
        "count": len(results),
        "message": f"Found {len(results)} furniture items"
    }