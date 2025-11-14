from typing import Any, List
from app.models.analysis import AnalysisArea


# This file is the "optional beauty dataset" plug-in.
# Right now it's a stub so the backend still runs.


def get_aesthetic_embedding(image: Any) -> Any:
    """
    TODO:
    - load MEBeauty / SCUT-FBP5500-pretrained model
    - run forward pass → get feature vector (not a beauty score)
    For now we just return None.
    """
    return None


def rerank_by_embedding(areas: List[AnalysisArea], embedding: Any) -> List[AnalysisArea]:
    """
    If we have an embedding, we could prioritize certain areas.
    For MVP, just return as-is.
    """
    return areas

