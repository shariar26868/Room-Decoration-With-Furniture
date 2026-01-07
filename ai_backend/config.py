"""
Configuration & Constants
=========================
"""

import os
from typing import Dict, List
from dotenv import load_dotenv
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
FAL_API_KEY = os.getenv("FAL_API_KEY")
# Product Database
# PRODUCT_API_URL = "http://206.162.244.175:5008/api/v1/products"
PRODUCT_API_URL = "http://72.60.126.182:5000/api/v1/products"

# Themes with Websites
THEMES: Dict[str, List[str]] = {
    "MINIMAL SCANDINAVIAN": [
        "ethnicraft.com", "kavehome.com", "nordicnest.com", "nordicknots.com",
        "swyfthome.com", "boconcept.com", "zarahome.com", "fermliving.com", "heals.com"
    ],
    "TIMELESS LUXURY": [
        "rh.com", "nordicknots.com", "eichholtz.com", "loaf.com", "portaromana.com",
        "cultfurniture.com", "dusk.com", "oka.com", "kavehome.com"
    ],
    "MODERN LIVING": [
        "liangandeimil.com", "eichholtz.com", "gillmorespace.com", "nordicknots.com",
        "cultfurniture.com", "sohohome.com", "swooneditions.com", "heals.com",
        "ligne-roset.com", "loopandtwist.com", "kavehome.com"
    ],
    "MODERN MEDITERRANEAN": [
        "zarahome.com", "loopandtwist.com", "swyfthome.com", "nordicknots.com", "kavehome.com"
    ],
    "BOHO ECLECTIC": [
        "sklum.com", "loopandtwist.com", "dusk.com", "cultfurniture.com",
        "heals.com", "kavehome.com", "perchandparrow.com"
    ]
}

# Room Types
ROOM_TYPES = [
    "Living Room Furniture",
    "Bedroom Furniture",
    "Dining Room Furniture",
    "Kitchen",
    "Home Office Furniture",
    "Balcony Furniture",
    "Kids Room Furniture",
    "Study Room",
    "Guest Bedroom"
]

# Space Calculation
MAX_ROOM_USAGE_PERCENT = 60
MIN_WALKWAY_SPACE = 36

# Image Generation
DALLE_MODEL = "dall-e-3"
DALLE_SIZE = "1024x1024"
DALLE_QUALITY = "standard"