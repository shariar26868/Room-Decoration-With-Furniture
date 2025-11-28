# """
# AI Space Calculator
# ===================
# Intelligent furniture placement feasibility using GPT-4
# """

# import logging
# import json
# from openai import OpenAI
# from typing import List, Dict
# from ai_backend.config import OPENAI_API_KEY, MAX_ROOM_USAGE_PERCENT

# logger = logging.getLogger(__name__)
# client = OpenAI(api_key=OPENAI_API_KEY)


# class SpaceCalculator:
#     """AI-powered space calculation and validation"""
    
#     @staticmethod
#     def calculate_room_area(length: float, width: float) -> float:
#         """Calculate room area in square feet"""
#         return length * width
    
#     @staticmethod
#     def calculate_cubic_volume(length: float, width: float, height: float) -> float:
#         """Calculate room volume in cubic feet"""
#         return length * width * height
    
#     @staticmethod
#     def estimate_furniture_size(furniture_type: str, subtype: str, room_sqft: float) -> Dict[str, float]:
#         """
#         Use GPT-4 to estimate realistic furniture dimensions
#         Returns estimated dimensions in inches
#         """
        
#         prompt = f"""You are an interior design expert. Estimate realistic dimensions for this furniture.

# Furniture: {subtype} ({furniture_type})
# Room Size: {room_sqft:.1f} square feet

# Provide typical dimensions in inches as JSON (no markdown, just JSON):
# {{
#     "width": <number>,
#     "depth": <number>,
#     "height": <number>,
#     "notes": "<brief explanation>"
# }}

# Examples:
# - Queen Bed in 200 sqft bedroom: {{"width": 60, "depth": 80, "height": 48, "notes": "Standard queen"}}
# - 3-Seater Sofa in 250 sqft living room: {{"width": 84, "depth": 38, "height": 36, "notes": "Standard 3-seater"}}
# - Dining Table (6-seater) in 180 sqft: {{"width": 72, "depth": 36, "height": 30, "notes": "6-person table"}}

# Consider:
# 1. Standard furniture sizes for this type
# 2. Room proportions (furniture should fit comfortably)
# 3. Typical manufacturer dimensions

# Respond ONLY with valid JSON, no other text."""

#         try:
#             response = client.chat.completions.create(
#                 model="gpt-4o",
#                 messages=[
#                     {"role": "system", "content": "You are a furniture dimension expert. Respond only with valid JSON."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 temperature=0.3
#             )
            
#             # Parse response
#             result_text = response.choices[0].message.content.strip()
            
#             # Clean up response (remove markdown if present)
#             result_text = result_text.replace("```json", "").replace("```", "").strip()
            
#             result = json.loads(result_text)
            
#             # Calculate square feet from dimensions
#             sqft = (result["width"] * result["depth"]) / 144.0  # sq inches to sq feet
#             result["sqft"] = round(sqft, 2)
            
#             logger.info(f"📐 {subtype}: {result['width']}\"W x {result['depth']}\"D = {sqft:.2f} sqft")
            
#             return result
            
#         except Exception as e:
#             logger.error(f"❌ GPT dimension estimation failed: {e}")
            
#             # Fallback to conservative estimates
#             return SpaceCalculator._fallback_dimensions(furniture_type, subtype)
    
#     @staticmethod
#     def _fallback_dimensions(furniture_type: str, subtype: str) -> Dict[str, float]:
#         """Fallback dimensions if GPT fails"""
        
#         # Conservative default estimates
#         type_lower = furniture_type.lower()
#         subtype_lower = subtype.lower()
        
#         # Determine dimensions based on keywords
#         if "sofa" in type_lower or "sofa" in subtype_lower:
#             if "sectional" in subtype_lower or "l-shape" in subtype_lower:
#                 dims = {"width": 120, "depth": 90, "height": 36}
#             elif "3-seater" in subtype_lower or "three" in subtype_lower:
#                 dims = {"width": 84, "depth": 38, "height": 36}
#             elif "2-seater" in subtype_lower or "two" in subtype_lower or "loveseat" in subtype_lower:
#                 dims = {"width": 60, "depth": 36, "height": 34}
#             else:
#                 dims = {"width": 78, "depth": 36, "height": 36}
        
#         elif "bed" in type_lower or "bed" in subtype_lower:
#             if "king" in subtype_lower:
#                 dims = {"width": 76, "depth": 80, "height": 48}
#             elif "queen" in subtype_lower:
#                 dims = {"width": 60, "depth": 80, "height": 48}
#             elif "double" in subtype_lower or "full" in subtype_lower:
#                 dims = {"width": 54, "depth": 75, "height": 48}
#             elif "single" in subtype_lower or "twin" in subtype_lower:
#                 dims = {"width": 39, "depth": 75, "height": 48}
#             else:
#                 dims = {"width": 60, "depth": 80, "height": 48}
        
#         elif "table" in type_lower or "table" in subtype_lower:
#             if "dining" in type_lower or "dining" in subtype_lower:
#                 if "8" in subtype_lower or "eight" in subtype_lower:
#                     dims = {"width": 96, "depth": 42, "height": 30}
#                 elif "6" in subtype_lower or "six" in subtype_lower:
#                     dims = {"width": 72, "depth": 36, "height": 30}
#                 else:
#                     dims = {"width": 60, "depth": 36, "height": 30}
#             elif "coffee" in subtype_lower:
#                 dims = {"width": 48, "depth": 24, "height": 18}
#             else:
#                 dims = {"width": 48, "depth": 30, "height": 30}
        
#         elif "chair" in type_lower or "chair" in subtype_lower:
#             if "dining" in subtype_lower:
#                 dims = {"width": 20, "depth": 22, "height": 36}
#             else:
#                 dims = {"width": 32, "depth": 34, "height": 36}
        
#         elif "desk" in type_lower or "desk" in subtype_lower:
#             dims = {"width": 48, "depth": 24, "height": 30}
        
#         elif "dresser" in type_lower or "dresser" in subtype_lower:
#             dims = {"width": 48, "depth": 20, "height": 48}
        
#         elif "bookshelf" in type_lower or "bookcase" in type_lower:
#             dims = {"width": 36, "depth": 12, "height": 72}
        
#         elif "nightstand" in type_lower or "bedside" in type_lower:
#             dims = {"width": 24, "depth": 18, "height": 24}
        
#         else:
#             # Generic fallback
#             dims = {"width": 36, "depth": 24, "height": 36}
        
#         # Calculate square feet
#         dims["sqft"] = round((dims["width"] * dims["depth"]) / 144.0, 2)
#         dims["notes"] = "Estimated dimensions"
        
#         return dims
    
#     @staticmethod
#     def validate_furniture_fit(
#         room_length: float,
#         room_width: float,
#         room_sqft: float,
#         current_furniture: List[Dict],
#         new_furniture: Dict
#     ) -> Dict:
#         """
#         Validate if new furniture fits in room
        
#         Returns validation result with usage statistics
#         """
        
#         # Calculate current usage
#         current_sqft = sum(item.get("sqft", 0) for item in current_furniture)
#         new_sqft = new_furniture.get("sqft", 0)
#         total_sqft = current_sqft + new_sqft
        
#         # Calculate usage percentage
#         usage_percent = (total_sqft / room_sqft) * 100
#         remaining_sqft = room_sqft - total_sqft
        
#         # Check if it fits
#         fits = usage_percent <= MAX_ROOM_USAGE_PERCENT
        
#         if fits:
#             message = f"✅ Furniture fits! Room usage: {usage_percent:.1f}% ({remaining_sqft:.1f} sqft free)"
#         else:
#             over_percent = usage_percent - MAX_ROOM_USAGE_PERCENT
#             message = f"❌ Room too crowded! Usage would be {usage_percent:.1f}% (exceeds max by {over_percent:.1f}%). Please remove items."
        
#         logger.info(message)
        
#         return {
#             "fits": fits,
#             "usage_percent": round(usage_percent, 2),
#             "total_sqft": round(total_sqft, 2),
#             "remaining_sqft": round(remaining_sqft, 2),
#             "max_usage": MAX_ROOM_USAGE_PERCENT,
#             "message": message
#         }
    
#     @staticmethod
#     def get_placement_suggestions(
#         room_length: float,
#         room_width: float,
#         furniture_items: List[Dict]
#     ) -> str:
#         """Generate AI-powered placement suggestions"""
        
#         furniture_list = "\n".join([
#             f"- {item.get('subtype', 'Item')}: {item.get('width', 0)}\"W x {item.get('depth', 0)}\"D"
#             for item in furniture_items
#         ])
        
#         prompt = f"""You are an interior designer. Suggest optimal furniture placement.

# Room: {room_length}' x {room_width}'

# Furniture:
# {furniture_list}

# Provide 3-4 short, actionable placement tips. Consider:
# - Traffic flow (3 feet walkways)
# - Natural focal points
# - Balance and symmetry
# - Functionality

# Be specific and practical."""

#         try:
#             response = client.chat.completions.create(
#                 model="gpt-4o",
#                 messages=[
#                     {"role": "system", "content": "You are an interior designer providing concise placement advice."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 temperature=0.7,
#                 max_tokens=200
#             )
            
#             return response.choices[0].message.content.strip()
            
#         except Exception as e:
#             logger.error(f"❌ Placement suggestion failed: {e}")
#             return "Place larger furniture against walls, maintain 3-foot walkways, and arrange seating to create conversation areas."





"""
AI Space Calculator
===================
Intelligent furniture placement using ONLY GPT-4 (no manual dimensions)
"""

import logging
import json
from openai import OpenAI
from typing import List, Dict
from ai_backend.config import OPENAI_API_KEY, MAX_ROOM_USAGE_PERCENT

logger = logging.getLogger(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)


class SpaceCalculator:
    """AI-powered space calculation and validation"""
    
    @staticmethod
    def calculate_room_area(length: float, width: float) -> float:
        """Calculate room area in square feet"""
        return length * width
    
    @staticmethod
    def calculate_cubic_volume(length: float, width: float, height: float) -> float:
        """Calculate room volume in cubic feet"""
        return length * width * height
    
    @staticmethod
    def estimate_furniture_size(furniture_type: str, subtype: str, room_sqft: float) -> Dict[str, float]:
        """
        Use ONLY GPT-4 to estimate furniture dimensions
        NO manual fallback - pure AI estimation
        
        Returns estimated dimensions in inches
        """
        
        prompt = f"""You are an interior design expert. Estimate realistic dimensions for this furniture.

Furniture Type: {furniture_type}
Furniture Subtype: {subtype}
Room Size: {room_sqft:.1f} square feet

Provide typical dimensions in inches as JSON (no markdown, just JSON):
{{
    "width": <number>,
    "depth": <number>,
    "height": <number>,
    "notes": "<brief explanation>"
}}

Real-world examples for reference:
- Queen Bed: {{"width": 60, "depth": 80, "height": 48, "notes": "Standard queen size"}}
- 3-Seater Sofa: {{"width": 84, "depth": 38, "height": 36, "notes": "Standard 3-seater"}}
- Dining Table (6-seater): {{"width": 72, "depth": 36, "height": 30, "notes": "6-person table"}}
- Coffee Table: {{"width": 48, "depth": 24, "height": 18, "notes": "Standard coffee table"}}
- Nightstand: {{"width": 24, "depth": 18, "height": 24, "notes": "Bedside table"}}
- Bookshelf: {{"width": 36, "depth": 12, "height": 72, "notes": "Standard bookcase"}}
- Office Desk: {{"width": 48, "depth": 24, "height": 30, "notes": "Standard desk"}}

Important considerations:
1. Use standard furniture industry dimensions
2. Ensure furniture is proportional to room size
3. Dimensions should be realistic and purchasable
4. Consider typical manufacturer specifications

Respond ONLY with valid JSON, no other text."""

        try:
            logger.info(f"🤖 Asking GPT-4 to estimate dimensions for: {subtype} ({furniture_type})")
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a furniture dimension expert with deep knowledge of interior design standards. Always provide realistic, industry-standard dimensions. Respond only with valid JSON."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            # Parse response
            result_text = response.choices[0].message.content.strip()
            
            # Clean up response (remove markdown if present)
            result_text = result_text.replace("```json", "").replace("```", "").strip()
            
            result = json.loads(result_text)
            
            # Validate required fields
            if not all(k in result for k in ["width", "depth", "height"]):
                raise ValueError("GPT response missing required dimensions")
            
            # Convert to float and validate
            width = float(result["width"])
            depth = float(result["depth"])
            height = float(result["height"])
            
            # Sanity check: dimensions should be reasonable
            if width <= 0 or width > 240:  # Max 20 feet width
                raise ValueError(f"Unrealistic width: {width}")
            if depth <= 0 or depth > 240:  # Max 20 feet depth
                raise ValueError(f"Unrealistic depth: {depth}")
            if height <= 0 or height > 120:  # Max 10 feet height
                raise ValueError(f"Unrealistic height: {height}")
            
            # Calculate square feet from dimensions
            sqft = (width * depth) / 144.0  # Convert sq inches to sq feet
            
            result["width"] = width
            result["depth"] = depth
            result["height"] = height
            result["sqft"] = round(sqft, 2)
            
            logger.info(f"✅ GPT-4 estimated: {width}\"W × {depth}\"D × {height}\"H = {sqft:.2f} sqft")
            logger.info(f"   Notes: {result.get('notes', 'N/A')}")
            
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Failed to parse GPT response as JSON: {e}")
            logger.error(f"   Raw response: {result_text[:200]}")
            raise Exception(f"AI dimension estimation failed - invalid JSON response")
        
        except ValueError as e:
            logger.error(f"❌ Invalid dimensions from GPT: {e}")
            raise Exception(f"AI dimension estimation failed - {str(e)}")
        
        except Exception as e:
            logger.error(f"❌ GPT dimension estimation failed: {e}")
            raise Exception(f"AI dimension estimation failed - please try again")
    
    @staticmethod
    def validate_furniture_fit(
        room_length: float,
        room_width: float,
        room_sqft: float,
        current_furniture: List[Dict],
        new_furniture: Dict
    ) -> Dict:
        """
        Validate if new furniture fits in room
        
        Returns validation result with usage statistics
        """
        
        # Calculate current usage
        current_sqft = sum(item.get("sqft", 0) for item in current_furniture)
        new_sqft = new_furniture.get("sqft", 0)
        total_sqft = current_sqft + new_sqft
        
        # Calculate usage percentage
        usage_percent = (total_sqft / room_sqft) * 100
        remaining_sqft = room_sqft - total_sqft
        
        # Check if it fits
        fits = usage_percent <= MAX_ROOM_USAGE_PERCENT
        
        if fits:
            message = f"✅ Furniture fits! Room usage: {usage_percent:.1f}% ({remaining_sqft:.1f} sqft free)"
        else:
            over_percent = usage_percent - MAX_ROOM_USAGE_PERCENT
            message = f"❌ Room too crowded! Usage would be {usage_percent:.1f}% (exceeds max by {over_percent:.1f}%). Please remove items."
        
        logger.info(message)
        
        return {
            "fits": fits,
            "usage_percent": round(usage_percent, 2),
            "total_sqft": round(total_sqft, 2),
            "remaining_sqft": round(remaining_sqft, 2),
            "max_usage": MAX_ROOM_USAGE_PERCENT,
            "message": message
        }
    
    @staticmethod
    def get_placement_suggestions(
        room_length: float,
        room_width: float,
        furniture_items: List[Dict]
    ) -> str:
        """Generate AI-powered placement suggestions"""
        
        furniture_list = "\n".join([
            f"- {item.get('subtype', 'Item')}: {item.get('width', 0)}\"W × {item.get('depth', 0)}\"D"
            for item in furniture_items
        ])
        
        prompt = f"""You are an interior designer. Suggest optimal furniture placement.

Room Dimensions: {room_length}' × {room_width}' ({room_length * room_width:.1f} sqft)

Furniture to arrange:
{furniture_list}

Provide 3-4 short, actionable placement tips. Consider:
- Traffic flow (minimum 3 feet walkways)
- Natural focal points (windows, doors)
- Balance and visual symmetry
- Functional layout and usability

Be specific and practical."""

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an interior designer providing concise, actionable placement advice."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=250
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"❌ Placement suggestion failed: {e}")
            return "Place larger furniture against walls to maximize floor space. Maintain 36-inch walkways between furniture. Arrange seating to create conversation areas facing each other. Consider natural light sources when positioning items."