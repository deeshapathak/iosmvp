# Rhinovate Quick Start Guide

Complete setup guide for both iOS app and backend API.

## Backend Setup

### 1. Install Python Dependencies

```bash
cd /Users/deeshapathak/iosmvp
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start the Backend Server

```bash
uvicorn app.main:app --reload
```

The API will be running at:
- **API**: http://127.0.0.1:8000
- **Docs**: http://127.0.0.1:8000/docs

### 3. Test the Backend

```bash
# Health check
curl http://127.0.0.1:8000/

# Test scan endpoint (if you have a test file)
curl -X POST http://127.0.0.1:8000/analyze-scan \
  -F "file=@test_scan.usdz"
```

## iOS App Setup

### 1. Open in Xcode

1. Create a new iOS App project in Xcode:
   - Product Name: `RhinovateApp`
   - Interface: `SwiftUI`
   - Language: `Swift`
   - Minimum Deployment: `iOS 13.0`

2. Add all files from this repository to your Xcode project
   - Delete default `ContentView.swift` and `AppNameApp.swift`
   - Drag all folders (Models, Services, Views, AR) into Xcode
   - Make sure "Copy items if needed" is checked

### 2. Update API Endpoint

Edit `Services/APIClient.swift`:

```swift
private let baseURL = URL(string: "http://127.0.0.1:8000")!  // Change for your server
```

For testing on a physical device, use your Mac's local IP:
```swift
private let baseURL = URL(string: "http://192.168.1.XXX:8000")!  // Your Mac's IP
```

### 3. Configure Permissions

Add to `Info.plist` (or in Xcode Target → Info):
- `Privacy - Camera Usage Description`: "We need camera access to scan your face for AI analysis."
- `Privacy - Face ID Usage Description`: "Face tracking is used to capture a 3D model of your face."

### 4. Build and Run

- Connect a physical iPhone (ARKit doesn't work in simulator)
- Select your device in Xcode
- Build and run (⌘R)

## Testing the Full Flow

1. **Start backend**: `uvicorn app.main:app --reload`
2. **Open iOS app** on your device
3. **Tap "Scan my face"**
4. **Position face** in view until "Face detected! Ready to capture."
5. **Tap "Capture"**
6. **Wait for upload** → results should appear

## Troubleshooting

### Backend won't start
- Check Python version: `python3 --version` (need 3.7+)
- Verify dependencies: `pip list | grep fastapi`
- Check port 8000 is free: `lsof -i :8000`

### iOS app can't connect
- Verify backend is running
- Check network: Use Mac's IP address for physical device
- Verify CORS is enabled in backend
- Check console logs in Xcode

### ARKit not working
- Must use physical device (iPhone X or newer)
- Check camera permissions are granted
- Verify Info.plist has Face ID usage description

## Next Steps

- Update backend URL for production deployment
- Add actual 3D scan processing (currently uses placeholders)
- Integrate ML models for aesthetic scoring
- Add user authentication and scan history

For detailed documentation:
- Backend: See `BACKEND_README.md`
- iOS: See `README.md` and `XCODE_SETUP.md`

