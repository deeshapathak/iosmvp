import os
import uuid
from fastapi import UploadFile
from app.core.config import settings
from app.services.facial_analysis import analyze_landmarks
from app.models.analysis import AnalysisResult


async def save_scan_and_analyze(file: UploadFile) -> AnalysisResult:
    """
    Save 3D scan → (later) extract landmarks from it → run same analysis.
    For now we fake landmarks so the iOS app always gets a valid response.
    """
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_id = str(uuid.uuid4())
    ext = file.filename.split(".")[-1]
    dest_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}.{ext}")

    content = await file.read()
    with open(dest_path, "wb") as f:
        f.write(content)

    # TODO: run 3D → landmarks here
    # For now, use placeholder single landmark to keep API working
    fake_landmarks = [{"x": 0.0, "y": 0.0, "z": 0.0}]
    result = analyze_landmarks(fake_landmarks)
    return result

