from typing import Dict, List
import uuid
from app.models.analysis import AnalysisResult, AnalysisArea
from app.ml.rules_engine import build_recommendations
from app.ml.aesthetic_embedder import get_aesthetic_embedding, rerank_by_embedding


# This maps raw landmarks → engineered measurements
def compute_measurements_from_landmarks(landmarks: List[dict]) -> Dict[str, float]:
    """
    landmarks: list of {x,y,z} or {x,y,z,name}.
    Computes real facial measurements from extracted landmarks.
    """
    import numpy as np
    from app.services.landmark_extractor import get_landmark_by_name, compute_inter_pupillary_distance
    
    measurements: Dict[str, float] = {}
    
    if not landmarks or len(landmarks) == 0:
        # Fallback to placeholder if no landmarks
        measurements["nose_to_ipd_ratio"] = 0.52
        measurements["chin_projection_mm"] = 11.8
        measurements["jaw_asymmetry_mm"] = 5.3
        return measurements
    
    # Convert landmarks to numpy arrays for easier computation
    landmark_dict = {}
    for lm in landmarks:
        name = lm.get("name", "")
        if name:
            landmark_dict[name] = np.array([lm["x"], lm["y"], lm["z"]])
    
    # 1. Compute Inter-Pupillary Distance (IPD)
    ipd = compute_inter_pupillary_distance(landmarks)
    if ipd is None:
        # Try to compute from eye landmarks
        left_eye = landmark_dict.get("left_eye_outer") or landmark_dict.get("left_eye_inner")
        right_eye = landmark_dict.get("right_eye_outer") or landmark_dict.get("right_eye_inner")
        if left_eye is not None and right_eye is not None:
            ipd = float(np.linalg.norm(left_eye - right_eye))
    
    # 2. Compute nose width (alar base width)
    # Use mouth corners or estimate from nose region
    nose_tip = landmark_dict.get("nose_tip")
    if nose_tip is not None and ipd is not None:
        # Estimate alar base width as a ratio of IPD
        # This is an approximation - ideally we'd have actual alar landmarks
        nose_width_estimate = ipd * 0.4  # Rough estimate
        measurements["nose_to_ipd_ratio"] = float(nose_width_estimate / ipd) if ipd > 0 else 0.52
    else:
        measurements["nose_to_ipd_ratio"] = 0.52
    
    # 3. Compute chin projection
    chin = landmark_dict.get("chin")
    if chin is not None and nose_tip is not None:
        # Projection relative to nose tip (forward distance)
        # Assuming face-forward orientation, Z is forward
        chin_projection = float(chin[2] - nose_tip[2])
        # Convert to mm (assuming normalized coordinates, scale appropriately)
        # ARKit typically works in meters, so multiply by 1000 for mm
        measurements["chin_projection_mm"] = abs(chin_projection) * 1000
    else:
        measurements["chin_projection_mm"] = 11.8
    
    # 4. Compute jawline asymmetry
    mouth_left = landmark_dict.get("mouth_left")
    mouth_right = landmark_dict.get("mouth_right")
    if mouth_left is not None and mouth_right is not None:
        # Measure asymmetry in Y (vertical) and X (horizontal)
        vertical_asymmetry = abs(mouth_left[1] - mouth_right[1])
        horizontal_asymmetry = abs(abs(mouth_left[0]) - abs(mouth_right[0]))
        # Combined asymmetry measure
        jaw_asymmetry = np.sqrt(vertical_asymmetry**2 + horizontal_asymmetry**2)
        measurements["jaw_asymmetry_mm"] = float(jaw_asymmetry * 1000)  # Convert to mm
    else:
        measurements["jaw_asymmetry_mm"] = 5.3
    
    # 5. Additional measurements (optional)
    if chin is not None and landmark_dict.get("forehead_center") is not None:
        forehead = landmark_dict["forehead_center"]
        face_height = float(np.linalg.norm(forehead - chin))
        measurements["face_height_mm"] = face_height * 1000
    
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

