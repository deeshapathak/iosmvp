#!/usr/bin/env python3
"""
Simple script to test scan access from a computer.
Run this after uploading scans from the iOS app.
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"


def list_scans():
    """List all uploaded scans."""
    print("📋 Listing all scans...")
    response = requests.get(f"{BASE_URL}/scans/")
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Found {data['total']} scan(s):\n")
        for scan in data['scans']:
            uploaded = datetime.fromisoformat(scan['uploaded_at'].replace('Z', '+00:00'))
            print(f"  ID: {scan['id']}")
            print(f"  Filename: {scan['filename']}")
            print(f"  Size: {scan['file_size']:,} bytes")
            print(f"  Format: {scan['format']}")
            print(f"  Uploaded: {uploaded.strftime('%Y-%m-%d %H:%M:%S')}")
            if scan.get('device'):
                print(f"  Device: {scan['device']}")
            print(f"  Download: {BASE_URL}/scans/{scan['id']}/download")
            print()
        return data['scans']
    else:
        print(f"❌ Error: {response.status_code}")
        return []


def download_scan(scan_id, output_filename=None):
    """Download a specific scan."""
    print(f"⬇️  Downloading scan {scan_id}...")
    response = requests.get(f"{BASE_URL}/scans/{scan_id}/download")
    if response.status_code == 200:
        filename = output_filename or f"scan_{scan_id}.usdz"
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"✅ Downloaded to: {filename}")
        return filename
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        return None


def get_scan_info(scan_id):
    """Get metadata for a specific scan."""
    print(f"ℹ️  Getting info for scan {scan_id}...")
    response = requests.get(f"{BASE_URL}/scans/{scan_id}")
    if response.status_code == 200:
        scan = response.json()
        print(json.dumps(scan, indent=2, default=str))
        return scan
    else:
        print(f"❌ Error: {response.status_code}")
        return None


if __name__ == "__main__":
    import sys
    
    print("🔍 Rhinovate Scan Access Test\n")
    print(f"Server: {BASE_URL}\n")
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "list":
            list_scans()
        elif command == "download" and len(sys.argv) > 2:
            scan_id = sys.argv[2]
            output = sys.argv[3] if len(sys.argv) > 3 else None
            download_scan(scan_id, output)
        elif command == "info" and len(sys.argv) > 2:
            scan_id = sys.argv[2]
            get_scan_info(scan_id)
        else:
            print("Usage:")
            print("  python test_scan_access.py list")
            print("  python test_scan_access.py download <scan_id> [output_filename]")
            print("  python test_scan_access.py info <scan_id>")
    else:
        # Default: list all scans
        scans = list_scans()
        if scans:
            print("\n💡 Tip: Use these commands to interact with scans:")
            print(f"  python test_scan_access.py download {scans[0]['id']}")
            print(f"  python test_scan_access.py info {scans[0]['id']}")

