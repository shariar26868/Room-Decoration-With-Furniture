"""
AI Interior Designer API
========================
Main FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from ai_backend.api import upload, selection, furniture, generation
from ai_backend.services.aws_service import init_aws_service
from ai_backend.services.product_service import ProductService
from ai_backend.config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_S3_BUCKET,
    AWS_REGION,
    PRODUCT_API_URL
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

product_service = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global product_service
    
    logger.info("🚀 Starting AI Interior Designer API")
    
    # Initialize AWS S3
    init_aws_service(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_BUCKET, AWS_REGION)
    logger.info("✅ AWS S3 initialized")
    
    # Initialize Product Service
    product_service = ProductService(PRODUCT_API_URL)
    await product_service.initialize()
    logger.info(f"✅ Product Database: {product_service.get_stats()}")
    
    app.state.product_service = product_service
    
    yield
    
    logger.info("🛑 Shutting down")


app = FastAPI(
    title="AI Interior Designer API",
    version="2.0.0",
    description="AI-powered interior design with 25,000+ real products",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(upload.router, prefix="/api/upload", tags=["1. Upload"])
app.include_router(selection.router, prefix="/api/selection", tags=["2. Selection"])
app.include_router(furniture.router, prefix="/api/furniture", tags=["3. Furniture"])
app.include_router(generation.router, prefix="/api/generation", tags=["4. Generation"])


@app.get("/")
async def root():
    return {
        "name": "AI Interior Designer API",
        "version": "2.0.0",
        "products": product_service.total_products if product_service else 0,
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "products": product_service.total_products if product_service else 0
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)