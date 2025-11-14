from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.analysis import AnalysisResult
from app.models.landmarks import LandmarkRequest
from app.services.facial_analysis import analyze_landmarks
from app.services.storage import save_scan_and_analyze


router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/landmarks", response_model=AnalysisResult)
async def analyze_from_landmarks(payload: LandmarkRequest):
    """
    iOS → MediaPipe → this endpoint.
    Send: { "landmarks": [{x,y,z}, ...], "device": "iPhone..." }
    """
    if not payload.landmarks:
        raise HTTPException(status_code=400, detail="No landmarks provided")

    result = analyze_landmarks([lm.dict() for lm in payload.landmarks])
    return result


@router.post("/scan", response_model=AnalysisResult)
async def analyze_from_scan(file: UploadFile = File(...)):
    """
    iOS → ARKit → upload 3D scan (usdz/obj/glb).
    For now we store and run a stub analysis.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    result = await save_scan_and_analyze(file)
    return result

