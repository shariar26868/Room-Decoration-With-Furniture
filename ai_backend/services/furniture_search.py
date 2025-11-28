"""
Furniture Search Service
========================
Search and match furniture from product database
"""

import logging
from typing import List, Dict
from ai_backend.models import FurnitureItem
from ai_backend.services.product_service import ProductService

logger = logging.getLogger(__name__)


def search_furniture_from_database(
    product_service: ProductService,
    furniture_selections: List[Dict],
    theme_websites: List[str],
    min_price: float,
    max_price: float
) -> List[FurnitureItem]:
    """
    Search for furniture products from database
    
    Args:
        product_service: Product database service
        furniture_selections: List of selected furniture with types/subtypes
        theme_websites: List of theme-specific websites
        min_price: Minimum price
        max_price: Maximum price
    
    Returns:
        List of matching FurnitureItem objects
    """
    
    results = []
    
    for selection in furniture_selections:
        furniture_type = selection.get("type")
        furniture_subtype = selection.get("subtype")
        
        logger.info(f"\n🔍 Searching for: {furniture_subtype} ({furniture_type})")
        
        # Search products
        products = product_service.search_products(
            furniture_type=furniture_type,
            furniture_subtype=furniture_subtype,
            theme_websites=theme_websites,
            min_price=min_price,
            max_price=max_price,
            limit=3  # Return top 3 matches per item
        )
        
        # Convert to FurnitureItem
        for product in products:
            item = FurnitureItem(
                name=product.get("productName", "Unknown Product"),
                link=product.get("productLink", ""),
                price=product.get("priceUSD", 0),
                image_url=product.get("productImage", ""),
                website=_extract_domain(product.get("websiteLink", "")),
                type=furniture_type,
                subtype=furniture_subtype
            )
            results.append(item)
            
            logger.info(f"  ✅ {item.name} - ${item.price:.0f} from {item.website}")
    
    logger.info(f"\n✅ Total products found: {len(results)}")
    
    return results


def _extract_domain(url: str) -> str:
    """Extract clean domain from URL"""
    if not url:
        return ""
    domain = url.replace("https://", "").replace("http://", "")
    domain = domain.split("/")[0]
    domain = domain.replace("www.", "")
    return domain