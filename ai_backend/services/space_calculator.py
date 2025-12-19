# """
# AI Space Calculator
# ===================
# Intelligent furniture placement using square feet consistently
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
#         Use GPT-4 to estimate furniture floor space
#         Returns dimensions in FEET and area in SQUARE FEET
#         """
        
#         prompt = f"""You are an interior design expert. Estimate realistic dimensions for this furniture.

# Furniture Type: {furniture_type}
# Furniture Subtype: {subtype}
# Room Size: {room_sqft:.1f} square feet

# Provide typical dimensions in FEET as JSON (no markdown, just JSON):
# {{
#     "width_ft": <width in feet>,
#     "depth_ft": <depth in feet>,
#     "height_ft": <height in feet>,
#     "notes": "<brief explanation>"
# }}

# Real-world examples for reference (in FEET):
# - Queen Bed: {{"width_ft": 5.0, "depth_ft": 6.7, "height_ft": 4.0, "notes": "Standard queen size (60x80 inches)"}}
# - 3-Seater Sofa: {{"width_ft": 7.0, "depth_ft": 3.2, "height_ft": 3.0, "notes": "Standard 3-seater (84x38 inches)"}}
# - Dining Table (6-seater): {{"width_ft": 6.0, "depth_ft": 3.0, "height_ft": 2.5, "notes": "6-person table (72x36 inches)"}}
# - Coffee Table: {{"width_ft": 4.0, "depth_ft": 2.0, "height_ft": 1.5, "notes": "Standard coffee table (48x24 inches)"}}
# - Nightstand: {{"width_ft": 2.0, "depth_ft": 1.5, "height_ft": 2.0, "notes": "Bedside table (24x18 inches)"}}
# - Bookshelf: {{"width_ft": 3.0, "depth_ft": 1.0, "height_ft": 6.0, "notes": "Standard bookcase (36x12 inches)"}}
# - Office Desk: {{"width_ft": 4.0, "depth_ft": 2.0, "height_ft": 2.5, "notes": "Standard desk (48x24 inches)"}}

# Important:
# 1. Dimensions should be in FEET (not inches)
# 2. Must be proportional to room size
# 3. Should match typical furniture store measurements
# 4. Floor footprint (width × depth) is most critical

# Respond ONLY with valid JSON, no other text."""

#         try:
#             logger.info(f"🤖 GPT-4 estimating dimensions for: {subtype} ({furniture_type})")
            
#             response = client.chat.completions.create(
#                 model="gpt-4o",
#                 messages=[
#                     {
#                         "role": "system", 
#                         "content": "You are a furniture dimension expert. Provide dimensions in FEET. Respond only with valid JSON."
#                     },
#                     {"role": "user", "content": prompt}
#                 ],
#                 temperature=0.3,
#                 max_tokens=200
#             )
            
#             # Parse response
#             result_text = response.choices[0].message.content.strip()
            
#             # Clean up response
#             result_text = result_text.replace("```json", "").replace("```", "").strip()
            
#             result = json.loads(result_text)
            
#             # Validate required fields
#             if not all(k in result for k in ["width_ft", "depth_ft", "height_ft"]):
#                 raise ValueError("GPT response missing required dimensions")
            
#             # Convert to float and validate
#             width_ft = float(result["width_ft"])
#             depth_ft = float(result["depth_ft"])
#             height_ft = float(result["height_ft"])
            
#             # Sanity check: dimensions should be reasonable
#             if width_ft <= 0 or width_ft > 20:  # Max 20 feet width
#                 raise ValueError(f"Unrealistic width: {width_ft} feet")
#             if depth_ft <= 0 or depth_ft > 20:  # Max 20 feet depth
#                 raise ValueError(f"Unrealistic depth: {depth_ft} feet")
#             if height_ft <= 0 or height_ft > 10:  # Max 10 feet height
#                 raise ValueError(f"Unrealistic height: {height_ft} feet")
            
#             # Calculate floor area (square feet)
#             sqft = width_ft * depth_ft
            
#             result["width_ft"] = round(width_ft, 2)
#             result["depth_ft"] = round(depth_ft, 2)
#             result["height_ft"] = round(height_ft, 2)
#             result["sqft"] = round(sqft, 2)
            
#             logger.info(f"✅ Dimensions: {width_ft:.1f}' W × {depth_ft:.1f}' D × {height_ft:.1f}' H = {sqft:.2f} sqft")
#             logger.info(f"   Notes: {result.get('notes', 'N/A')}")
            
#             return result
            
#         except json.JSONDecodeError as e:
#             logger.error(f"❌ Failed to parse GPT response as JSON: {e}")
#             logger.error(f"   Raw response: {result_text[:200]}")
#             raise Exception(f"AI dimension estimation failed - invalid JSON response")
        
#         except ValueError as e:
#             logger.error(f"❌ Invalid dimensions from GPT: {e}")
#             raise Exception(f"AI dimension estimation failed - {str(e)}")
        
#         except Exception as e:
#             logger.error(f"❌ GPT dimension estimation failed: {e}")
#             raise Exception(f"AI dimension estimation failed - please try again")
    
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
#         All calculations in square feet
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
#             message = f"✅ Furniture fits! Room usage: {usage_percent:.1f}% ({remaining_sqft:.1f} sqft remaining)"
#         else:
#             over_percent = usage_percent - MAX_ROOM_USAGE_PERCENT
#             message = f"❌ Room too crowded! Usage would be {usage_percent:.1f}% (exceeds {MAX_ROOM_USAGE_PERCENT}% by {over_percent:.1f}%)"
        
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
#             f"- {item.get('subtype', 'Item')}: {item.get('width_ft', 0):.1f}' W × {item.get('depth_ft', 0):.1f}' D ({item.get('sqft', 0):.1f} sqft)"
#             for item in furniture_items
#         ])
        
#         prompt = f"""You are an interior designer. Suggest optimal furniture placement.

# Room Dimensions: {room_length}' × {room_width}' = {room_length * room_width:.1f} sqft

# Furniture to arrange:
# {furniture_list}

# Provide 3-4 short, actionable placement tips. Consider:
# - Traffic flow (minimum 3 feet walkways)
# - Natural focal points (windows, doors)
# - Balance and visual symmetry
# - Functional layout and usability

# Be specific and practical."""

#         try:
#             response = client.chat.completions.create(
#                 model="gpt-4o",
#                 messages=[
#                     {"role": "system", "content": "You are an interior designer providing concise placement advice."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 temperature=0.7,
#                 max_tokens=250
#             )
            
#             return response.choices[0].message.content.strip()
            
#         except Exception as e:
#             logger.error(f"❌ Placement suggestion failed: {e}")
#             return "Place larger furniture against walls. Maintain 3-foot walkways. Create conversation areas with seating. Consider natural light when positioning."






# """
# AI Space Calculator
# ===================
# Intelligent furniture placement using square inches consistently
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
#         """Calculate room area in square inches"""
#         return length * width
    
#     @staticmethod
#     def calculate_cubic_volume(length: float, width: float, height: float) -> float:
#         """Calculate room volume in cubic inches"""
#         return length * width * height
    
#     @staticmethod
#     def estimate_furniture_size(furniture_type: str, subtype: str, room_sqin: float) -> Dict[str, float]:
#         """
#         Use GPT-4 to estimate furniture floor space
#         Returns dimensions in INCHES and area in SQUARE INCHES
#         """
        
#         prompt = f"""You are an interior design expert. Estimate realistic dimensions for this furniture.

# Furniture Type: {furniture_type}
# Furniture Subtype: {subtype}
# Room Size: {room_sqin:.1f} square inches

# Provide typical dimensions in INCHES as JSON (no markdown, just JSON):
# {{
#     "width_in": <width in inches>,
#     "depth_in": <depth in inches>,
#     "height_in": <height in inches>,
#     "notes": "<brief explanation>"
# }}

# Real-world examples for reference (in INCHES):
# - Queen Bed: {{"width_in": 60, "depth_in": 80, "height_in": 48, "notes": "Standard queen size"}}
# - 3-Seater Sofa: {{"width_in": 84, "depth_in": 38, "height_in": 36, "notes": "Standard 3-seater"}}
# - Dining Table (6-seater): {{"width_in": 72, "depth_in": 36, "height_in": 30, "notes": "6-person table"}}
# - Coffee Table: {{"width_in": 48, "depth_in": 24, "height_in": 18, "notes": "Standard coffee table"}}
# - Nightstand: {{"width_in": 24, "depth_in": 18, "height_in": 24, "notes": "Bedside table"}}
# - Bookshelf: {{"width_in": 36, "depth_in": 12, "height_in": 72, "notes": "Standard bookcase"}}
# - Office Desk: {{"width_in": 48, "depth_in": 24, "height_in": 30, "notes": "Standard desk"}}

# Important:
# 1. Dimensions should be in INCHES (not feet)
# 2. Must be proportional to room size
# 3. Should match typical furniture store measurements
# 4. Floor footprint (width × depth) is most critical

# Respond ONLY with valid JSON, no other text."""

#         try:
#             logger.info(f"🤖 GPT-4 estimating dimensions for: {subtype} ({furniture_type})")
            
#             response = client.chat.completions.create(
#                 model="gpt-4o",
#                 messages=[
#                     {
#                         "role": "system", 
#                         "content": "You are a furniture dimension expert. Provide dimensions in INCHES. Respond only with valid JSON."
#                     },
#                     {"role": "user", "content": prompt}
#                 ],
#                 temperature=0.3,
#                 max_tokens=200
#             )
            
#             # Parse response
#             result_text = response.choices[0].message.content.strip()
            
#             # Clean up response
#             result_text = result_text.replace("```json", "").replace("```", "").strip()
            
#             result = json.loads(result_text)
            
#             # Validate required fields
#             if not all(k in result for k in ["width_in", "depth_in", "height_in"]):
#                 raise ValueError("GPT response missing required dimensions")
            
#             # Convert to float and validate
#             width_in = float(result["width_in"])
#             depth_in = float(result["depth_in"])
#             height_in = float(result["height_in"])
            
#             # Sanity check: dimensions should be reasonable
#             if width_in <= 0 or width_in > 240:  # Max 240 inches (20 feet)
#                 raise ValueError(f"Unrealistic width: {width_in} inches")
#             if depth_in <= 0 or depth_in > 240:  # Max 240 inches (20 feet)
#                 raise ValueError(f"Unrealistic depth: {depth_in} inches")
#             if height_in <= 0 or height_in > 120:  # Max 120 inches (10 feet)
#                 raise ValueError(f"Unrealistic height: {height_in} inches")
            
#             # Calculate floor area (square inches)
#             sqin = width_in * depth_in
            
#             result["width_in"] = round(width_in, 2)
#             result["depth_in"] = round(depth_in, 2)
#             result["height_in"] = round(height_in, 2)
#             result["sqin"] = round(sqin, 2)
            
#             logger.info(f"✅ Dimensions: {width_in:.1f}\" W × {depth_in:.1f}\" D × {height_in:.1f}\" H = {sqin:.2f} sqin")
#             logger.info(f"   Notes: {result.get('notes', 'N/A')}")
            
#             return result
            
#         except json.JSONDecodeError as e:
#             logger.error(f"❌ Failed to parse GPT response as JSON: {e}")
#             logger.error(f"   Raw response: {result_text[:200]}")
#             raise Exception(f"AI dimension estimation failed - invalid JSON response")
        
#         except ValueError as e:
#             logger.error(f"❌ Invalid dimensions from GPT: {e}")
#             raise Exception(f"AI dimension estimation failed - {str(e)}")
        
#         except Exception as e:
#             logger.error(f"❌ GPT dimension estimation failed: {e}")
#             raise Exception(f"AI dimension estimation failed - please try again")
    
#     @staticmethod
#     def validate_furniture_fit(
#         room_length: float,
#         room_width: float,
#         room_sqin: float,
#         current_furniture: List[Dict],
#         new_furniture: Dict
#     ) -> Dict:
#         """
#         Validate if new furniture fits in room
#         All calculations in square inches
#         """
        
#         # Calculate current usage
#         current_sqin = sum(item.get("sqin", 0) for item in current_furniture)
#         new_sqin = new_furniture.get("sqin", 0)
#         total_sqin = current_sqin + new_sqin
        
#         # Calculate usage percentage
#         usage_percent = (total_sqin / room_sqin) * 100
#         remaining_sqin = room_sqin - total_sqin
        
#         # Check if it fits
#         fits = usage_percent <= MAX_ROOM_USAGE_PERCENT
        
#         if fits:
#             message = f"✅ Furniture fits! Room usage: {usage_percent:.1f}% ({remaining_sqin:.1f} sqin remaining)"
#         else:
#             over_percent = usage_percent - MAX_ROOM_USAGE_PERCENT
#             message = f"❌ Room too crowded! Usage would be {usage_percent:.1f}% (exceeds {MAX_ROOM_USAGE_PERCENT}% by {over_percent:.1f}%)"
        
#         logger.info(message)
        
#         return {
#             "fits": fits,
#             "usage_percent": round(usage_percent, 2),
#             "total_sqin": round(total_sqin, 2),
#             "remaining_sqin": round(remaining_sqin, 2),
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
#             f"- {item.get('subtype', 'Item')}: {item.get('width_in', 0):.1f}\" W × {item.get('depth_in', 0):.1f}\" D ({item.get('sqin', 0):.1f} sqin)"
#             for item in furniture_items
#         ])
        
#         prompt = f"""You are an interior designer. Suggest optimal furniture placement.

# Room Dimensions: {room_length}\" × {room_width}\" = {room_length * room_width:.1f} sqin

# Furniture to arrange:
# {furniture_list}

# Provide 3-4 short, actionable placement tips. Consider:
# - Traffic flow (minimum 36 inches walkways)
# - Natural focal points (windows, doors)
# - Balance and visual symmetry
# - Functional layout and usability

# Be specific and practical."""

#         try:
#             response = client.chat.completions.create(
#                 model="gpt-4o",
#                 messages=[
#                     {"role": "system", "content": "You are an interior designer providing concise placement advice."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 temperature=0.7,
#                 max_tokens=250
#             )
            
#             return response.choices[0].message.content.strip()
            
#         except Exception as e:
#             logger.error(f"❌ Placement suggestion failed: {e}")
#             return "Place larger furniture against walls. Maintain 36-inch walkways. Create conversation areas with seating. Consider natural light when positioning."








"""
AI Space Calculator
===================
Intelligent furniture placement using square centimeters consistently
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
        """Calculate room area in square centimeters"""
        return length * width
    
    @staticmethod
    def calculate_cubic_volume(length: float, width: float, height: float) -> float:
        """Calculate room volume in cubic centimeters"""
        return length * width * height
    
    @staticmethod
    def estimate_furniture_size(furniture_type: str, subtype: str, room_sqcm: float) -> Dict[str, float]:
        """
        Use GPT-4 to estimate furniture floor space
        Returns dimensions in CENTIMETERS and area in SQUARE CENTIMETERS
        """
        
        prompt = f"""You are an interior design expert. Estimate realistic dimensions for this furniture.

Furniture Type: {furniture_type}
Furniture Subtype: {subtype}
Room Size: {room_sqcm:.1f} square centimeters

Provide typical dimensions in CENTIMETERS as JSON (no markdown, just JSON):
{{
    "width_cm": <width in centimeters>,
    "depth_cm": <depth in centimeters>,
    "height_cm": <height in centimeters>,
    "notes": "<brief explanation>"
}}

Real-world examples for reference (in CENTIMETERS):
- Queen Bed: {{"width_cm": 152, "depth_cm": 203, "height_cm": 122, "notes": "Standard queen size (152x203 cm)"}}
- 3-Seater Sofa: {{"width_cm": 213, "depth_cm": 97, "height_cm": 91, "notes": "Standard 3-seater (213x97 cm)"}}
- Dining Table (6-seater): {{"width_cm": 183, "depth_cm": 91, "height_cm": 76, "notes": "6-person table (183x91 cm)"}}
- Coffee Table: {{"width_cm": 122, "depth_cm": 61, "height_cm": 46, "notes": "Standard coffee table (122x61 cm)"}}
- Nightstand: {{"width_cm": 61, "depth_cm": 46, "height_cm": 61, "notes": "Bedside table (61x46 cm)"}}
- Bookshelf: {{"width_cm": 91, "depth_cm": 30, "height_cm": 183, "notes": "Standard bookcase (91x30 cm)"}}
- Office Desk: {{"width_cm": 122, "depth_cm": 61, "height_cm": 76, "notes": "Standard desk (122x61 cm)"}}
- Dining Chair: {{"width_cm": 46, "depth_cm": 51, "height_cm": 91, "notes": "Standard chair (46x51 cm)"}}
- Wardrobe: {{"width_cm": 122, "depth_cm": 61, "height_cm": 213, "notes": "Standard wardrobe (122x61 cm)"}}
- Side Table: {{"width_cm": 46, "depth_cm": 46, "height_cm": 56, "notes": "Small side table (46x46 cm)"}}

Important:
1. Dimensions should be in CENTIMETERS (not inches or feet)
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
                        "content": "You are a furniture dimension expert. Provide dimensions in CENTIMETERS. Respond only with valid JSON."
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
            if not all(k in result for k in ["width_cm", "depth_cm", "height_cm"]):
                raise ValueError("GPT response missing required dimensions")
            
            # Convert to float and validate
            width_cm = float(result["width_cm"])
            depth_cm = float(result["depth_cm"])
            height_cm = float(result["height_cm"])
            
            # Sanity check: dimensions should be reasonable
            if width_cm <= 0 or width_cm > 600:  # Max 600 cm (20 feet)
                raise ValueError(f"Unrealistic width: {width_cm} cm")
            if depth_cm <= 0 or depth_cm > 600:  # Max 600 cm (20 feet)
                raise ValueError(f"Unrealistic depth: {depth_cm} cm")
            if height_cm <= 0 or height_cm > 300:  # Max 300 cm (10 feet)
                raise ValueError(f"Unrealistic height: {height_cm} cm")
            
            # Calculate floor area (square centimeters)
            sqcm = width_cm * depth_cm
            
            result["width_cm"] = round(width_cm, 2)
            result["depth_cm"] = round(depth_cm, 2)
            result["height_cm"] = round(height_cm, 2)
            result["sqcm"] = round(sqcm, 2)
            
            logger.info(f"✅ Dimensions: {width_cm:.1f} cm W × {depth_cm:.1f} cm D × {height_cm:.1f} cm H = {sqcm:.2f} sq cm")
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
        room_sqcm: float,
        current_furniture: List[Dict],
        new_furniture: Dict
    ) -> Dict:
        """
        Validate if new furniture fits in room
        All calculations in square centimeters
        """
        
        # Calculate current usage
        current_sqcm = sum(item.get("sqcm", 0) for item in current_furniture)
        new_sqcm = new_furniture.get("sqcm", 0)
        total_sqcm = current_sqcm + new_sqcm
        
        # Calculate usage percentage
        usage_percent = (total_sqcm / room_sqcm) * 100
        remaining_sqcm = room_sqcm - total_sqcm
        
        # Check if it fits
        fits = usage_percent <= MAX_ROOM_USAGE_PERCENT
        
        if fits:
            message = f"✅ Furniture fits! Room usage: {usage_percent:.1f}% ({remaining_sqcm:.1f} sq cm remaining)"
        else:
            over_percent = usage_percent - MAX_ROOM_USAGE_PERCENT
            message = f"❌ Room too crowded! Usage would be {usage_percent:.1f}% (exceeds {MAX_ROOM_USAGE_PERCENT}% by {over_percent:.1f}%)"
        
        logger.info(message)
        
        return {
            "fits": fits,
            "usage_percent": round(usage_percent, 2),
            "total_sqcm": round(total_sqcm, 2),
            "remaining_sqcm": round(remaining_sqcm, 2),
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
            f"- {item.get('subtype', 'Item')}: {item.get('width_cm', 0):.1f} cm W × {item.get('depth_cm', 0):.1f} cm D ({item.get('sqcm', 0):.1f} sq cm)"
            for item in furniture_items
        ])
        
        prompt = f"""You are an interior designer. Suggest optimal furniture placement.

Room Dimensions: {room_length} cm × {room_width} cm = {room_length * room_width:.1f} sq cm

Furniture to arrange:
{furniture_list}

Provide 3-4 short, actionable placement tips. Consider:
- Traffic flow (minimum 90 cm walkways)
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
            return "Place larger furniture against walls. Maintain 90 cm walkways. Create conversation areas with seating. Consider natural light when positioning."