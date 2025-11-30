# 🎨 AI Interior Designer API

AI-powered interior design system that composes real furniture products into room images using GPT-4 Vision, background removal, and intelligent placement.

---

## 🚀 Features

### Core Features
- ✅ **Room Image Upload** - Upload any room photo
- ✅ **25,000+ Real Products** - Search from actual furniture databases
- ✅ **5 Design Themes** - Minimal Scandinavian, Timeless Luxury, Modern Living, etc.
- ✅ **AI Space Validation** - GPT-4 estimates furniture dimensions and validates room capacity
- ✅ **Smart Product Search** - Theme-aware furniture matching with price filtering
- ✅ **Background Removal** - Automatic furniture background removal using rembg
- ✅ **GPT-4 Vision Placement** - AI-powered furniture positioning in rooms
- ✅ **Custom Decorative Items** - Upload wall clocks, lamps, paintings, etc.
- ✅ **Bulk Furniture Selection** - Add multiple items at once

### Technical Features
- FastAPI backend with async support
- AWS S3 image storage
- OpenAI GPT-4 Vision integration
- Automated background removal (rembg)
- RESTful API with Swagger documentation
- Docker containerization
- Session-based state management

---

## 📋 Prerequisites

- **Docker** and **Docker Compose** installed
- **OpenAI API Key** (for GPT-4 Vision)
- **AWS S3 Account** (for image storage)
- **Replicate API Key** (optional, for advanced inpainting)

---

## ⚡ Quick Start

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd Room-Decoration-With-Furniture
```

### 2. Create `.env` File
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
# OpenAI
OPENAI_API_KEY=sk-proj-xxx

# AWS S3
AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AWS_S3_BUCKET=room-decor
AWS_REGION=eu-north-1

# Replicate (Optional)
REPLICATE_API_TOKEN=r8_xxxxxxxxxxxxxxxxxxxxxxxx

# Pexels (Optional)
PEXELS_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. Build and Run with Docker
```bash
# Build the image
docker-compose build

# Start the service
docker-compose up -d

# Check logs
docker-compose logs -f
```

### 4. Access the API
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 🏗️ Project Structure

```
Room-Decoration-With-Furniture/
├── main.py                          # FastAPI entry point
├── Dockerfile                       # Docker image definition
├── docker-compose.yml               # Docker Compose configuration
├── requirements.txt                 # Python dependencies
├── .env                            # Environment variables (create this)
├── .dockerignore                   # Docker ignore rules
│
└── ai_backend/
    ├── __init__.py
    ├── config.py                   # Configuration & constants
    ├── models.py                   # Pydantic models
    │
    ├── api/                        # API endpoints
    │   ├── upload.py              # Room image upload
    │   ├── selection.py           # Room/theme/furniture selection
    │   ├── furniture.py           # Product search
    │   ├── decorative.py          # Custom decorative items
    │   └── generation.py          # Image generation
    │
    └── services/                   # Business logic
        ├── aws_service.py         # S3 upload
        ├── product_service.py     # Product database
        ├── space_calculator.py    # AI space validation
        ├── furniture_search.py    # Product search logic
        ├── image_compositor.py    # Image composition
        ├── image_generator.py     # Generation orchestration
        └── storage.py             # File storage utilities
```

---

## 📖 API Workflow

### Step 1: Upload Room Image
```bash
POST /api/upload/upload
Content-Type: multipart/form-data

room_image: [file]
```

**Response:**
```json
{
  "success": true,
  "session_id": "abc-123-def-456",
  "image_url": "https://s3.../room.jpg"
}
```

---

### Step 2: Select Room Type
```bash
POST /api/selection/room-type
{
  "session_id": "abc-123-def-456",
  "room_type": "Living Room Furniture"
}
```

---

### Step 3: Select Theme
```bash
POST /api/selection/theme
{
  "session_id": "abc-123-def-456",
  "theme": "MINIMAL SCANDINAVIAN"
}
```

---

### Step 3.5: Get Available Furniture (Optional)
```bash
GET /api/selection/available-furniture/{session_id}
```

**Response:**
```json
{
  "furniture_catalog": {
    "Sofas": ["2-seater sofa", "3-seater sofa", "Corner sofa"],
    "Tables": ["Coffee table", "Side table", "Console table"],
    "Chairs": ["Armchair", "Dining chair", "Accent chair"]
  },
  "total_types": 15,
  "total_products": 1250
}
```

---

### Step 4: Set Room Dimensions
```bash
POST /api/selection/dimensions
{
  "session_id": "abc-123-def-456",
  "length": 15.0,
  "width": 12.0,
  "height": 9.0
}
```

---

### Step 5: Select Furniture (Bulk)
```bash
POST /api/selection/furniture/select-bulk
{
  "session_id": "abc-123-def-456",
  "furniture_items": [
    {"furniture_type": "Sofas", "subtype": "3-Seater Sofa"},
    {"furniture_type": "Tables", "subtype": "Coffee Table"},
    {"furniture_type": "Chairs", "subtype": "Armchair"}
  ]
}
```

**Response:**
```json
{
  "success": true,
  "total_added": 3,
  "room_usage_percent": 21.5,
  "remaining_sqft": 141.3,
  "message": "Added 3 items successfully"
}
```

---

### Step 6: Set Price Range
```bash
POST /api/furniture/price-range
{
  "session_id": "abc-123-def-456",
  "min_price": 500,
  "max_price": 5000
}
```

---

### Step 7: Search Products
```bash
POST /api/furniture/search
{
  "session_id": "abc-123-def-456"
}
```

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "name": "Allegro 3-Seater Sofa",
      "price": 2899,
      "image_url": "https://...",
      "link": "https://...",
      "website": "oka.com",
      "type": "Sofas",
      "subtype": "3-Seater Sofa"
    },
    // ... more products
  ],
  "count": 9
}
```

---

### Step 7.5: Upload Decorative Items (Optional)
```bash
POST /api/decorative/upload
Content-Type: multipart/form-data

session_id: "abc-123-def-456"
item_name: "Wall Clock"
placement_hint: "on wall above sofa"
item_image: [file]
```

---

### Step 8: Generate Final Design
```bash
POST /api/generation/generate
{
  "session_id": "abc-123-def-456",
  "furniture_links": [
    "https://oka.com/sofa-link",
    "https://heals.com/table-link",
    "https://cultfurniture.com/chair-link"
  ],
  "prompt": "Place sofa against left wall, coffee table in center, armchair on right side"
}
```

**Response:**
```json
{
  "success": true,
  "generated_image_url": "https://s3.../generated/final.png",
  "original_image_url": "https://s3.../rooms/original.jpg",
  "furniture_items": [...],
  "generation_time_seconds": 12.5,
  "message": "Room design with 3 furniture + 1 decorative items generated"
}
```

---

## 🎯 Available Themes

1. **MINIMAL SCANDINAVIAN** - Clean, simple, functional
2. **TIMELESS LUXURY** - Elegant, high-end, classic
3. **MODERN LIVING** - Contemporary, sleek, minimalist
4. **MODERN MEDITERRANEAN** - Warm, earthy, coastal
5. **BOHO ECLECTIC** - Colorful, artistic, mixed patterns

---

## 🛠️ Development

### Run Locally (Without Docker)
```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python main.py

# Or with uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Run Tests
```bash
pytest tests/
```

### View Logs
```bash
# Docker logs
docker-compose logs -f

# Specific service
docker-compose logs -f ai-interior-designer
```

---

## 🐳 Docker Commands

```bash
# Build image
docker-compose build

# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart services
docker-compose restart

# View logs
docker-compose logs -f

# Execute command in container
docker-compose exec ai-interior-designer bash

# Remove all containers and volumes
docker-compose down -v
```

---

## 📊 API Endpoints Summary

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/upload/upload` | POST | Upload room image |
| `/api/selection/room-type` | POST | Select room type |
| `/api/selection/theme` | POST | Select design theme |
| `/api/selection/available-furniture/{id}` | GET | Get available furniture |
| `/api/selection/dimensions` | POST | Set room dimensions |
| `/api/selection/furniture/select` | POST | Add single furniture |
| `/api/selection/furniture/select-bulk` | POST | Add multiple furniture |
| `/api/selection/furniture/list/{id}` | GET | List selected furniture |
| `/api/selection/furniture/clear/{id}` | DELETE | Clear all furniture |
| `/api/furniture/price-range` | POST | Set price range |
| `/api/furniture/search` | POST | Search products |
| `/api/decorative/upload` | POST | Upload decorative item |
| `/api/decorative/list/{id}` | GET | List decorative items |
| `/api/generation/generate` | POST | Generate final design |
| `/api/generation/history/{id}` | GET | View generation history |

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 Vision | ✅ Yes |
| `AWS_ACCESS_KEY_ID` | AWS access key | ✅ Yes |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | ✅ Yes |
| `AWS_S3_BUCKET` | S3 bucket name | ✅ Yes |
| `AWS_REGION` | AWS region | ✅ Yes |
| `REPLICATE_API_TOKEN` | Replicate API token | ⚠️ Optional |
| `PEXELS_API_KEY` | Pexels API key | ⚠️ Optional |

### Themes Configuration
Edit `ai_backend/config.py` to modify themes and websites.

---

## 🚨 Troubleshooting

### Issue: rembg not working
```bash
# Install rembg with ONNX runtime
pip install rembg onnxruntime

# Or in Docker, rebuild:
docker-compose build --no-cache
```

### Issue: S3 upload fails
- Check AWS credentials in `.env`
- Verify S3 bucket exists and is accessible
- Check bucket permissions (public access for generated images)

### Issue: GPT-4 Vision API errors
- Verify `OPENAI_API_KEY` is valid
- Check OpenAI API credits/quota
- Ensure image URLs are publicly accessible

### Issue: Port 8000 already in use
```bash
# Stop existing process
docker-compose down

# Or change port in docker-compose.yml
ports:
  - "8001:8000"  # Use port 8001 instead
```

---

## 📝 License

MIT License

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Check `/docs` for API documentation
- Review logs: `docker-compose logs -f`

---

## 🎉 Credits

Built with:
- FastAPI
- OpenAI GPT-4 Vision
- AWS S3
- rembg (background removal)
- Pillow (image processing)

---

**Happy Designing! 🎨✨**