"""
AI Space Calculator
===================
Intelligent furniture placement using square feet consistently
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
        Use GPT-4 to estimate furniture floor space
        Returns dimensions in FEET and area in SQUARE FEET
        """
        
        prompt = f"""You are an interior design expert. Estimate realistic dimensions for this furniture.

Furniture Type: {furniture_type}
Furniture Subtype: {subtype}
Room Size: {room_sqft:.1f} square feet

Provide typical dimensions in FEET as JSON (no markdown, just JSON):
{{
    "width_ft": <width in feet>,
    "depth_ft": <depth in feet>,
    "height_ft": <height in feet>,
    "notes": "<brief explanation>"
}}

Real-world examples for reference (in FEET):
- Queen Bed: {{"width_ft": 5.0, "depth_ft": 6.7, "height_ft": 4.0, "notes": "Standard queen size (60x80 inches)"}}
- 3-Seater Sofa: {{"width_ft": 7.0, "depth_ft": 3.2, "height_ft": 3.0, "notes": "Standard 3-seater (84x38 inches)"}}
- Dining Table (6-seater): {{"width_ft": 6.0, "depth_ft": 3.0, "height_ft": 2.5, "notes": "6-person table (72x36 inches)"}}
- Coffee Table: {{"width_ft": 4.0, "depth_ft": 2.0, "height_ft": 1.5, "notes": "Standard coffee table (48x24 inches)"}}
- Nightstand: {{"width_ft": 2.0, "depth_ft": 1.5, "height_ft": 2.0, "notes": "Bedside table (24x18 inches)"}}
- Bookshelf: {{"width_ft": 3.0, "depth_ft": 1.0, "height_ft": 6.0, "notes": "Standard bookcase (36x12 inches)"}}
- Office Desk: {{"width_ft": 4.0, "depth_ft": 2.0, "height_ft": 2.5, "notes": "Standard desk (48x24 inches)"}}

Important:
1. Dimensions should be in FEET (not inches)
2. Must be proportional to room size
3. Should match typical furniture store measurements
4. Floor footprint (width × depth) is most critical

Respond ONLY with valid JSON, no other text."""

        try:
            logger.info(f"🤖 GPT-4 estimating dimensions for: {subtype} ({furniture_type})")
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a furniture dimension expert. Provide dimensions in FEET. Respond only with valid JSON."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            # Parse response
            result_text = response.choices[0].message.content.strip()
            
            # Clean up response
            result_text = result_text.replace("```json", "").replace("```", "").strip()
            
            result = json.loads(result_text)
            
            # Validate required fields
            if not all(k in result for k in ["width_ft", "depth_ft", "height_ft"]):
                raise ValueError("GPT response missing required dimensions")
            
            # Convert to float and validate
            width_ft = float(result["width_ft"])
            depth_ft = float(result["depth_ft"])
            height_ft = float(result["height_ft"])
            
            # Sanity check: dimensions should be reasonable
            if width_ft <= 0 or width_ft > 20:  # Max 20 feet width
                raise ValueError(f"Unrealistic width: {width_ft} feet")
            if depth_ft <= 0 or depth_ft > 20:  # Max 20 feet depth
                raise ValueError(f"Unrealistic depth: {depth_ft} feet")
            if height_ft <= 0 or height_ft > 10:  # Max 10 feet height
                raise ValueError(f"Unrealistic height: {height_ft} feet")
            
            # Calculate floor area (square feet)
            sqft = width_ft * depth_ft
            
            result["width_ft"] = round(width_ft, 2)
            result["depth_ft"] = round(depth_ft, 2)
            result["height_ft"] = round(height_ft, 2)
            result["sqft"] = round(sqft, 2)
            
            logger.info(f"✅ Dimensions: {width_ft:.1f}' W × {depth_ft:.1f}' D × {height_ft:.1f}' H = {sqft:.2f} sqft")
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
        All calculations in square feet
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
            message = f"✅ Furniture fits! Room usage: {usage_percent:.1f}% ({remaining_sqft:.1f} sqft remaining)"
        else:
            over_percent = usage_percent - MAX_ROOM_USAGE_PERCENT
            message = f"❌ Room too crowded! Usage would be {usage_percent:.1f}% (exceeds {MAX_ROOM_USAGE_PERCENT}% by {over_percent:.1f}%)"
        
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
            f"- {item.get('subtype', 'Item')}: {item.get('width_ft', 0):.1f}' W × {item.get('depth_ft', 0):.1f}' D ({item.get('sqft', 0):.1f} sqft)"
            for item in furniture_items
        ])
        
        prompt = f"""You are an interior designer. Suggest optimal furniture placement.

Room Dimensions: {room_length}' × {room_width}' = {room_length * room_width:.1f} sqft

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
                    {"role": "system", "content": "You are an interior designer providing concise placement advice."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=250
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"❌ Placement suggestion failed: {e}")
            return "Place larger furniture against walls. Maintain 3-foot walkways. Create conversation areas with seating. Consider natural light when positioning."