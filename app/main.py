from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes_analysis
from app.services.storage import save_scan_and_analyze
from app.models.analysis import AnalysisResult

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


@app.get("/")
def read_root():
    return {"status": "ok", "service": "rhinovate"}


@app.post("/analyze-scan", response_model=AnalysisResult)
async def analyze_scan(file: UploadFile = File(...)):
    """
    Direct endpoint matching iOS app: POST /analyze-scan
    iOS → ARKit → upload 3D scan (usdz/obj/glb).
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    result = await save_scan_and_analyze(file)
    return result

