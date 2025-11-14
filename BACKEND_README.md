# Rhinovate Backend API

FastAPI backend for the Rhinovate iOS app. Handles 3D face scan uploads and returns AI-powered cosmetic analysis.

## Project Structure

```
app/
 ├── __init__.py
 ├── main.py                    # FastAPI app entry point
 ├── core/
 │    ├── __init__.py
 │    └── config.py             # Settings and configuration
 ├── models/
 │    ├── __init__.py
 │    ├── analysis.py           # AnalysisResult and AnalysisArea models
 │    └── landmarks.py          # Landmark request models
 ├── api/
 │    ├── __init__.py
 │    └── routes_analysis.py    # API routes
 ├── services/
 │    ├── __init__.py
 │    ├── facial_analysis.py    # Core analysis logic
 │    └── storage.py            # File upload handling
 └── ml/
     ├── __init__.py
     ├── rules_engine.py        # Rule-based recommendations
     └── aesthetic_embedder.py  # Placeholder for ML models
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or create a virtual environment first:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **API**: http://127.0.0.1:8000
- **Interactive Docs**: http://127.0.0.1:8000/docs
- **Alternative Docs**: http://127.0.0.1:8000/redoc

### 3. Environment Variables (Optional)

```bash
export UPLOAD_DIR="uploads"  # Directory for storing uploaded scans
export AESTHETIC_MODEL_PATH=""  # Path to ML model (if using)
```

## API Endpoints

### POST `/analyze-scan`

**iOS app endpoint** - Upload 3D face scan (USDZ/OBJ/GLB)

**Request:**
- Content-Type: `multipart/form-data`
- Field name: `file`
- File: 3D scan file (USDZ, OBJ, or GLB)

**Response:**
```json
{
  "id": "uuid",
  "analysis_summary": "We found 3 areas that can be harmonized.",
  "areas": [
    {
      "area": "Nose (alar base)",
      "issue": "Alar base slightly wide relative to inter-pupillary distance (ratio=0.52)",
      "suggestion": "Conservative alar base reduction to narrow nasal width",
      "show_simulation": true
    },
    {
      "area": "Chin",
      "issue": "Chin slightly under-projected (11.8mm)",
      "suggestion": "Increase chin projection by ~15% (implant or genioplasty)",
      "show_simulation": true
    }
  ]
}
```

**Example (curl):**
```bash
curl -X POST http://127.0.0.1:8000/analyze-scan \
  -F "file=@face_scan.usdz"
```

### POST `/analysis/landmarks`

Analyze from facial landmarks (for MediaPipe-based clients)

**Request:**
```json
{
  "landmarks": [
    {"x": 0.1, "y": 0.2, "z": 0.0},
    {"x": 0.2, "y": 0.3, "z": 0.0}
  ],
  "device": "iPhone",
  "image_id": "optional"
}
```

**Example (curl):**
```bash
curl -X POST http://127.0.0.1:8000/analysis/landmarks \
  -H "Content-Type: application/json" \
  -d '{
    "landmarks": [
      {"x": 0.1, "y": 0.2, "z": 0.0},
      {"x": 0.2, "y": 0.3, "z": 0.0}
    ],
    "device": "iPhone"
  }'
```

### GET `/`

Health check endpoint

**Response:**
```json
{
  "status": "ok",
  "service": "rhinovate"
}
```

## Testing

### Using curl

```bash
# Test scan upload
curl -X POST http://127.0.0.1:8000/analyze-scan \
  -F "file=@test_scan.usdz"

# Test landmarks
curl -X POST http://127.0.0.1:8000/analysis/landmarks \
  -H "Content-Type: application/json" \
  -d '{"landmarks": [{"x":0.1,"y":0.2,"z":0.0}], "device": "iPhone"}'
```

### Using FastAPI Interactive Docs

Visit http://127.0.0.1:8000/docs and use the interactive Swagger UI to test endpoints.

## Architecture

### Current Implementation (MVP)

1. **File Upload**: Saves 3D scans to `uploads/` directory
2. **Placeholder Analysis**: Uses fake landmarks to generate recommendations
3. **Rule Engine**: Simple threshold-based recommendations for:
   - Nose (alar base width)
   - Chin projection
   - Jawline asymmetry

### Future Enhancements

- **3D Processing**: Extract actual landmarks from USDZ/OBJ files
- **ML Models**: Integrate aesthetic scoring models (MEBeauty, SCUT-FBP5500)
- **MediaPipe**: Server-side landmark detection from images
- **Database**: Store scans and analysis history
- **Authentication**: User accounts and scan history

## Configuration

### CORS

Currently allows all origins (`allow_origins=["*"]`). For production, update in `app/main.py`:

```python
allow_origins=["https://yourdomain.com"]
```

### Upload Directory

Change via environment variable:
```bash
export UPLOAD_DIR="/path/to/uploads"
```

Or modify `app/core/config.py` directly.

## Deployment

### Development
```bash
uvicorn app.main:app --reload
```

### Production

Using Gunicorn with Uvicorn workers:
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker (Example)

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Notes

- The current implementation uses placeholder measurements for MVP
- USDZ files are saved but not processed yet (TODO: extract landmarks from 3D models)
- Rule-based engine uses simple thresholds; should be calibrated with surgeon input
- Aesthetic embedder is a stub; ready for ML model integration

## Troubleshooting

**Import errors?**
- Make sure you're in the project root directory
- Ensure all `__init__.py` files exist
- Check Python path includes the project directory

**CORS issues?**
- Verify CORS middleware is configured correctly
- Check that iOS app baseURL matches backend URL

**File upload fails?**
- Ensure `uploads/` directory exists and is writable
- Check file size limits (FastAPI default is 100MB)

**Port already in use?**
```bash
uvicorn app.main:app --reload --port 8001
```

