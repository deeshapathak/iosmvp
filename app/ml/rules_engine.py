from typing import List, Dict
from app.models.analysis import AnalysisArea


def build_recommendations(measurements: Dict[str, float]) -> List[AnalysisArea]:
    """
    Very simple rule-based engine.
    Replace thresholds with surgeon-provided ranges later.
    """
    recs: List[AnalysisArea] = []

    nose_ratio = measurements.get("nose_to_ipd_ratio")
    if nose_ratio is not None and nose_ratio > 0.5:
        recs.append(AnalysisArea(
            area="Nose (alar base)",
            issue=f"Alar base slightly wide relative to inter-pupillary distance (ratio={nose_ratio:.2f})",
            suggestion="Conservative alar base reduction to narrow nasal width",
            show_simulation=True
        ))

    chin_proj = measurements.get("chin_projection_mm")
    if chin_proj is not None and chin_proj < 12.5:
        recs.append(AnalysisArea(
            area="Chin",
            issue=f"Chin slightly under-projected ({chin_proj:.1f}mm)",
            suggestion="Increase chin projection by ~15% (implant or genioplasty)",
            show_simulation=True
        ))

    jaw_asym = measurements.get("jaw_asymmetry_mm")
    if jaw_asym is not None and jaw_asym > 3.0:
        recs.append(AnalysisArea(
            area="Jawline",
            issue=f"Jawline asymmetry of {jaw_asym:.1f}mm detected",
            suggestion="2.0mm lateral jawline correction to improve facial balance",
            show_simulation=True
        ))

    # You can add midface / brow / upper third rules here.

    return recs

