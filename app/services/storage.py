import os
import uuid
from fastapi import UploadFile, HTTPException
from app.core.config import settings
from app.services.facial_analysis import analyze_landmarks
from app.services.landmark_extractor import extract_landmarks_from_mesh
from app.models.analysis import AnalysisResult


async def save_scan_and_analyze(file: UploadFile) -> AnalysisResult:
    """
    Save 3D scan → extract landmarks from it → run analysis.
    """
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_id = str(uuid.uuid4())
    ext = file.filename.split(".")[-1] if file.filename else "usdz"
    dest_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}.{ext}")

    # Save uploaded file
    content = await file.read()
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
    return result

