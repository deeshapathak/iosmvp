# 📱➡️💻 End-to-End Scan Access Guide

Your iOS app now uploads 3D face scans, and you can access them from any computer!

## How It Works

1. **iOS App** → Scans face with ARKit → Uploads USDZ to `/analyze-scan`
2. **Backend** → Saves scan file + metadata → Returns analysis
3. **Computer** → Can list and download all scans via API

## API Endpoints

### 1. Upload Scan (iOS App)
**POST** `/analyze-scan`
- Uploads 3D scan file
- Returns analysis + scan ID
- Scan is automatically saved

### 2. List All Scans (Computer)
**GET** `/scans/`

Returns all uploaded scans:
```json
{
  "scans": [
    {
      "id": "abc-123-def",
      "filename": "face_scan.usdz",
      "file_size": 123456,
      "uploaded_at": "2025-11-15T10:30:00",
      "format": "usdz",
      "device": "iPhone 14 Pro",
      "analysis_id": "xyz-789"
    }
  ],
  "total": 1
}
```

### 3. Get Scan Metadata
**GET** `/scans/{scan_id}`

Get details about a specific scan.

### 4. Download Scan (Computer)
**GET** `/scans/{scan_id}/download`

Downloads the actual 3D file (USDZ/OBJ/GLB).

## Usage Examples

### From Browser

1. **List all scans:**
   ```
   http://127.0.0.1:8000/scans/
   ```

2. **Download a scan:**
   ```
   http://127.0.0.1:8000/scans/{scan_id}/download
   ```

### From Command Line (curl)

```bash
# List all scans
curl http://127.0.0.1:8000/scans/

# Download a specific scan
curl -O http://127.0.0.1:8000/scans/abc-123-def/download

# Or with a custom filename
curl -o my_scan.usdz http://127.0.0.1:8000/scans/abc-123-def/download
```

### From Python

```python
import requests

# List scans
response = requests.get("http://127.0.0.1:8000/scans/")
scans = response.json()
print(f"Total scans: {scans['total']}")

# Download a scan
scan_id = scans['scans'][0]['id']
response = requests.get(f"http://127.0.0.1:8000/scans/{scan_id}/download")
with open("downloaded_scan.usdz", "wb") as f:
    f.write(response.content)
```

### From JavaScript/Node.js

```javascript
// List scans
fetch('http://127.0.0.1:8000/scans/')
  .then(res => res.json())
  .then(data => {
    console.log(`Total scans: ${data.total}`);
    data.scans.forEach(scan => {
      console.log(`${scan.filename} - ${scan.uploaded_at}`);
    });
  });

// Download a scan
async function downloadScan(scanId) {
  const response = await fetch(`http://127.0.0.1:8000/scans/${scanId}/download`);
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'scan.usdz';
  a.click();
}
```

## Interactive API Docs

Visit **http://127.0.0.1:8000/docs** to:
- See all endpoints
- Test API calls directly
- View request/response schemas

## File Storage

- **Scans saved to**: `uploads/` directory (configurable via `UPLOAD_DIR`)
- **Metadata saved to**: `uploads/scans_metadata.json`
- **File naming**: `{scan_id}.{ext}` (e.g., `abc-123.usdz`)

## Complete Workflow

1. **User scans face on iPhone** → App uploads to `/analyze-scan`
2. **Backend processes** → Saves file + extracts landmarks + analyzes
3. **User gets results** → Analysis displayed in app
4. **Later, from computer**:
   - Visit `http://your-server:8000/scans/` to see all scans
   - Click download link or use API to get files
   - Open USDZ files in macOS Preview, Blender, or other 3D software

## Security Notes

⚠️ **For production:**
- Add authentication to `/scans/` endpoints
- Restrict CORS origins
- Add rate limiting
- Use HTTPS
- Consider user-based access control

## Troubleshooting

**"No scans found"**
- Make sure iOS app has uploaded at least one scan
- Check `uploads/` directory exists
- Verify `scans_metadata.json` exists

**"Scan not found"**
- Verify scan ID is correct
- Check if file still exists in `uploads/` directory

**Can't download**
- Check file permissions
- Verify file wasn't deleted manually
- Check server logs for errors

## Next Steps

- Add web UI to browse scans
- Add user authentication
- Add scan deletion endpoint
- Add scan search/filtering
- Add batch download

