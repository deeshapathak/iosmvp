"""
Manages scan metadata and file operations.
Stores scan information in a JSON file for simple persistence.
"""
import os
import json
from datetime import datetime
from typing import List, Optional
from app.models.scan import ScanMetadata
from app.core.config import settings


METADATA_FILE = os.path.join(settings.UPLOAD_DIR, "scans_metadata.json")


def load_metadata() -> List[ScanMetadata]:
    """Load all scan metadata from JSON file."""
    if not os.path.exists(METADATA_FILE):
        return []
    
    try:
        with open(METADATA_FILE, "r") as f:
            data = json.load(f)
            return [ScanMetadata(**item) for item in data]
    except Exception as e:
        print(f"Error loading metadata: {e}")
        return []


def save_metadata(metadata: ScanMetadata) -> None:
    """Save scan metadata to JSON file."""
    scans = load_metadata()
    scans.append(metadata)
    
    # Convert to dict for JSON serialization
    data = [scan.dict() for scan in scans]
    
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    with open(METADATA_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)


def get_scan_by_id(scan_id: str) -> Optional[ScanMetadata]:
    """Get scan metadata by ID."""
    scans = load_metadata()
    for scan in scans:
        if scan.id == scan_id:
            return scan
    return None


def get_all_scans() -> List[ScanMetadata]:
    """Get all scan metadata."""
    return load_metadata()


def create_scan_metadata(
    scan_id: str,
    filename: str,
    file_path: str,
    file_size: int,
    file_format: str,
    analysis_id: Optional[str] = None,
    device: Optional[str] = None
) -> ScanMetadata:
    """Create and save scan metadata."""
    metadata = ScanMetadata(
        id=scan_id,
        filename=filename,
        file_path=file_path,
        file_size=file_size,
        uploaded_at=datetime.now(),
        analysis_id=analysis_id,
        device=device,
        format=file_format
    )
    save_metadata(metadata)
    return metadata

