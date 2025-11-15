"""
API routes for managing and accessing 3D scans.
Allows listing and downloading scans from a computer.
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.models.scan import ScanListResponse
from app.services.scan_manager import get_all_scans, get_scan_by_id
import os


router = APIRouter(prefix="/scans", tags=["scans"])


@router.get("/", response_model=ScanListResponse)
async def list_scans():
    """
    List all uploaded 3D scans.
    Accessible from a computer to see all scans.
    """
    scans = get_all_scans()
    return ScanListResponse(
        scans=scans,
        total=len(scans)
    )


@router.get("/{scan_id}")
async def get_scan(scan_id: str):
    """
    Get scan metadata by ID.
    """
    scan = get_scan_by_id(scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scan


@router.get("/{scan_id}/download")
async def download_scan(scan_id: str):
    """
    Download a specific 3D scan file.
    Accessible from a computer to download the scan file.
    """
    scan = get_scan_by_id(scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    if not os.path.exists(scan.file_path):
        raise HTTPException(status_code=404, detail="Scan file not found on server")
    
    return FileResponse(
        path=scan.file_path,
        filename=scan.filename,
        media_type="application/octet-stream"
    )

