from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes_analysis, routes_scans
from app.services.storage import save_scan_and_analyze
from app.models.analysis import AnalysisResult
from typing import Optional

app = FastAPI(
    title="Rhinovate API",
    version="0.1.0",
    description="Backend for Rhinovate iOS app — analyzes landmarks or 3D scans and returns cosmetic suggestions."
)

# allow iOS simulator / device
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routes
app.include_router(routes_analysis.router)
app.include_router(routes_scans.router)


@app.get("/")
def read_root():
    return {
        "status": "ok",
        "service": "rhinovate",
        "endpoints": {
            "upload": "/analyze-scan",
            "list_scans": "/scans/",
            "download_scan": "/scans/{scan_id}/download"
        }
    }


@app.post("/analyze-scan", response_model=AnalysisResult)
async def analyze_scan(
    file: UploadFile = File(...),
    device: Optional[str] = Header(None, alias="X-Device")
):
    """
    Direct endpoint matching iOS app: POST /analyze-scan
    iOS → ARKit → upload 3D scan (usdz/obj/glb).
    
    The scan is saved and can be accessed later via /scans/ endpoints.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    result, scan_id = await save_scan_and_analyze(file, device=device)
    # Include scan_id in response for reference
    result.id = scan_id  # Use scan_id as the result ID so it can be used to download
    return result

