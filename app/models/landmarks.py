from pydantic import BaseModel
from typing import List, Optional


class Landmark(BaseModel):
    x: float
    y: float
    z: Optional[float] = None


class LandmarkRequest(BaseModel):
    landmarks: List[Landmark]
    device: Optional[str] = None
    # optional image or frame reference
    image_id: Optional[str] = None

