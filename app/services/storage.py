import os
import uuid
from typing import Tuple
from fastapi import UploadFile, HTTPException
from app.core.config import settings
from app.services.facial_analysis import analyze_landmarks
from app.services.landmark_extractor import extract_landmarks_from_mesh
from app.services.scan_manager import create_scan_metadata
from app.models.analysis import AnalysisResult


async def save_scan_and_analyze(file: UploadFile, device: str = None) -> Tuple[AnalysisResult, str]:
    """
    Save 3D scan → extract landmarks from it → run analysis.
    Returns: (AnalysisResult, scan_id)
    """
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    scan_id = str(uuid.uuid4())
    ext = file.filename.split(".")[-1] if file.filename else "usdz"
    dest_path = os.path.join(settings.UPLOAD_DIR, f"{scan_id}.{ext}")

    # Save uploaded file
    content = await file.read()
    file_size = len(content)
    with open(dest_path, "wb") as f:
        f.write(content)

    # Extract landmarks from 3D model
    try:
        landmarks = extract_landmarks_from_mesh(dest_path)
        
        if not landmarks or len(landmarks) == 0:
            # Fallback to placeholder if extraction fails
            landmarks = [{"x": 0.0, "y": 0.0, "z": 0.0}]
    except Exception as e:
        # Log error but continue with placeholder to keep API working
        print(f"Warning: Landmark extraction failed: {e}")
        landmarks = [{"x": 0.0, "y": 0.0, "z": 0.0}]
    
    # Run analysis with extracted landmarks
    result = analyze_landmarks(landmarks)
    
    # Save scan metadata
    create_scan_metadata(
        scan_id=scan_id,
        filename=file.filename or f"scan.{ext}",
        file_path=dest_path,
        file_size=file_size,
        file_format=ext,
        analysis_id=result.id,
        device=device
    )
    
    return result, scan_id

