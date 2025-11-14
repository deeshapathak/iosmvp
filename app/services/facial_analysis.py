from typing import Dict, List
import uuid
from app.models.analysis import AnalysisResult, AnalysisArea
from app.ml.rules_engine import build_recommendations
from app.ml.aesthetic_embedder import get_aesthetic_embedding, rerank_by_embedding


# This maps raw landmarks (MediaPipe indices) → engineered measurements
def compute_measurements_from_landmarks(landmarks: List[dict]) -> Dict[str, float]:
    """
    landmarks: list of {x,y,z}. MediaPipe Face Landmarker has a known index map.
    For MVP we use placeholder values — you can replace with actual index math later.
    """
    measurements: Dict[str, float] = {}

    # TODO: real math
    # Example:
    # nose_tip = landmarks[1]  # depends on model
    # left_eye_outer = landmarks[33]
    # right_eye_outer = landmarks[263]
    # compute IPD, etc.

    measurements["nose_to_ipd_ratio"] = 0.52
    measurements["chin_projection_mm"] = 11.8
    measurements["jaw_asymmetry_mm"] = 5.3

    return measurements


def analyze_landmarks(landmarks: List[dict]) -> AnalysisResult:
    """
    Core entry point for iOS.
    """
    # 1) geometry-based
    measurements = compute_measurements_from_landmarks(landmarks)

    # 2) rule-based recommendations
    recs = build_recommendations(measurements)

    # 3) optional: aesthetic embedding to reorder / prioritize
    embedding = get_aesthetic_embedding(None)  # we don't have image here yet
    recs = rerank_by_embedding(recs, embedding)

    summary = f"We found {len(recs)} areas that can be harmonized."
    return AnalysisResult(
        id=str(uuid.uuid4()),
        analysis_summary=summary,
        areas=recs
    )

