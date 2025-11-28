"""
Product Service
===============
Handles product database operations with intelligent filtering
"""

import httpx
import logging
from typing import List, Dict, Optional
from collections import defaultdict

logger = logging.getLogger(__name__)


class ProductService:
    """Manages product database with intelligent search"""
    
    def __init__(self, api_url: str):
        self.api_url = api_url
        self.products: List[Dict] = []
        self.by_website: Dict[str, List[Dict]] = defaultdict(list)
        self.by_type: Dict[str, List[Dict]] = defaultdict(list)
        self.by_subtype: Dict[str, Dict[str, List[Dict]]] = defaultdict(lambda: defaultdict(list))
        self.total_products = 0
        
    async def initialize(self):
        """Load and index all products from API"""
        logger.info(f"📦 Loading products from {self.api_url}")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(self.api_url)
                response.raise_for_status()
                
                data = response.json()
                self.products = data.get("data", [])
                self.total_products = len(self.products)
                
                logger.info(f"✅ Loaded {self.total_products} products")
                
                # Build indexes for fast lookup
                self._build_indexes()
                
        except Exception as e:
            logger.error(f"❌ Failed to load products: {e}")
            raise
    
    def _build_indexes(self):
        """Build search indexes by website, type, and subtype"""
        for product in self.products:
            # Index by website
            website = self._extract_domain(product.get("websiteLink", ""))
            self.by_website[website].append(product)
            
            # Index by type
            prod_type = product.get("type", "")
            self.by_type[prod_type].append(product)
            
            # Index by subtype within type
            subtype = product.get("subTypes", "")
            self.by_subtype[prod_type][subtype].append(product)
        
        logger.info(f"📊 Indexed: {len(self.by_website)} websites, {len(self.by_type)} types")
    
    def _extract_domain(self, url: str) -> str:
        """Extract clean domain from URL"""
        if not url:
            return ""
        
        # Remove protocol
        domain = url.replace("https://", "").replace("http://", "")
        
        # Remove path
        domain = domain.split("/")[0]
        
        # Remove www.
        domain = domain.replace("www.", "")
        
        return domain
    
    def search_products(
        self,
        furniture_type: str,
        furniture_subtype: str,
        theme_websites: List[str],
        min_price: float,
        max_price: float,
        limit: int = 5
    ) -> List[Dict]:
        """
        Search products with intelligent filtering
        
        Priority order:
        1. Products from theme websites
        2. Matching type and subtype
        3. Within price range (with tolerance)
        """
        
        logger.info(f"🔍 Searching: {furniture_type} > {furniture_subtype}")
        logger.info(f"   Price: ${min_price:.0f} - ${max_price:.0f}")
        
        # Get products matching type and subtype
        candidates = self.by_subtype.get(furniture_type, {}).get(furniture_subtype, [])
        
        if not candidates:
            # Fallback: search by type only
            logger.warning(f"⚠️ No exact subtype match, searching by type: {furniture_type}")
            candidates = self.by_type.get(furniture_type, [])
        
        if not candidates:
            logger.warning(f"⚠️ No products found for {furniture_type}")
            return []
        
        logger.info(f"   Found {len(candidates)} candidates")
        
        # Filter by price with tolerance
        price_tolerance = 0.25  # Allow 25% price variance
        in_budget = [
            p for p in candidates
            if (min_price * (1 - price_tolerance)) <= p.get("priceUSD", 0) <= (max_price * (1 + price_tolerance))
        ]
        
        logger.info(f"   {len(in_budget)} within budget (±25%)")
        
        if not in_budget:
            # Use all candidates if nothing in budget
            logger.warning(f"⚠️ No products in budget, using all candidates")
            in_budget = candidates
        
        # Prioritize theme websites
        theme_domains = [self._extract_domain(w) for w in theme_websites]
        
        priority_products = []
        other_products = []
        
        for product in in_budget:
            product_domain = self._extract_domain(product.get("websiteLink", ""))
            if product_domain in theme_domains:
                priority_products.append(product)
            else:
                other_products.append(product)
        
        logger.info(f"   ✨ {len(priority_products)} from theme websites")
        logger.info(f"   📦 {len(other_products)} from other websites")
        
        # Combine: theme products first
        results = priority_products + other_products
        
        # Return top results
        return results[:limit]
    
    def get_available_types(self) -> List[str]:
        """Get all available furniture types"""
        return list(self.by_type.keys())
    
    def get_available_subtypes(self, furniture_type: str) -> List[str]:
        """Get all available subtypes for a furniture type"""
        return list(self.by_subtype.get(furniture_type, {}).keys())
    
    def get_stats(self) -> str:
        """Get database statistics"""
        return f"{self.total_products} products, {len(self.by_website)} websites, {len(self.by_type)} categories"