from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ScanMetadata(BaseModel):
    """Metadata for a 3D face scan."""
    id: str
    filename: str
    file_path: str
    file_size: int  # in bytes
    uploaded_at: datetime
    analysis_id: Optional[str] = None  # Link to analysis result
    device: Optional[str] = None  # e.g., "iPhone 14 Pro"
    format: str  # "usdz", "obj", "glb", etc.


class ScanListResponse(BaseModel):
    """Response for listing scans."""
    scans: list[ScanMetadata]
    total: int

