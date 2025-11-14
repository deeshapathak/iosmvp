# Rhinovate iOS App

A 100% native iOS app built with SwiftUI and ARKit for facial scanning and AI-powered cosmetic analysis.

## Features

- **Native SwiftUI Interface** - No webviews, no Safari, everything runs natively
- **ARKit Face Scanning** - Captures 3D face mesh using ARKit face tracking
- **Backend Integration** - Uploads scans to Rhinovate API for AI analysis
- **In-App Results** - Displays AI recommendations directly in the app

## Project Structure

```
RhinovateApp/
 ├── RhinovateApp.swift          # App entry point
 ├── Models/
 │    └── AnalysisResult.swift   # Data models for API responses
 ├── Services/
 │    └── APIClient.swift        # Network layer for API calls
 ├── Views/
 │    ├── HomeView.swift         # Home screen with scan button
 │    ├── ScanView.swift         # SwiftUI wrapper for AR scanner
 │    └── ResultView.swift     # Results display screen
 └── AR/
      └── FaceScanViewController.swift  # ARKit face scanning controller
```

## Setup Instructions

### 1. Create Xcode Project

1. Open Xcode and create a new iOS App project
2. Name it "RhinovateApp"
3. Choose SwiftUI as the interface
4. Set minimum deployment target to iOS 13.0+ (ARKit face tracking requires Face ID device or iOS 13+)

### 2. Add Files to Project

Copy all the files from this repository into your Xcode project, maintaining the folder structure:
- Models/
- Services/
- Views/
- AR/

### 3. Configure Info.plist

The `Info.plist` file includes required permissions:
- `NSCameraUsageDescription` - For camera access
- `NSFaceIDUsageDescription` - For face tracking

### 4. Update API Endpoint

Edit `Services/APIClient.swift` and update the `baseURL` constant:

```swift
private let baseURL = URL(string: "https://api.rhinovate.ai")!
```

Change to your actual API endpoint.

### 5. Backend Requirements

Your backend API must accept:

**Endpoint:** `POST /analyze-scan`

**Request:**
- Content-Type: `multipart/form-data`
- Field name: `file`
- File format: USDZ (or OBJ/GLB if your backend supports it)

**Response:**
```json
{
  "analysis_summary": "We found 4 areas that could be harmonized.",
  "areas": [
    {
      "area": "Nose (dorsum)",
      "issue": "Dorsal height slightly above balanced profile line",
      "suggestion": "Conservative dorsal reduction",
      "show_simulation": true
    }
  ]
}
```

## Device Requirements

- iPhone with Face ID (iPhone X or newer)
- iOS 13.0 or later
- ARKit face tracking requires A12 Bionic chip or newer

## Features & Architecture

### Face Scanning
- Uses `ARFaceTrackingConfiguration` for real-time face mesh capture
- Exports face geometry as USDZ file
- Manual capture button for user control

### Networking
- Async/await based API client
- Multipart form-data file upload
- JSON response decoding

### User Flow
1. User opens app → sees home screen
2. Taps "Scan my face" → ARKit scanner opens
3. Positions face → taps "Capture"
4. App uploads scan → shows loading
5. Results displayed natively in SwiftUI

## Future Enhancements

- Cache scans locally for re-viewing
- Add 3D preview using SceneKit/Metal
- Add intensity slider for AI recommendations
- Support for full-head scans using LiDAR (ARWorldTrackingConfiguration)

## Troubleshooting

### ARKit not working?
- Ensure device has Face ID
- Check Info.plist permissions
- Verify iOS version is 13.0+

### Export fails?
- The app attempts multiple export methods
- Check console for specific error messages
- Ensure device has sufficient storage

### API upload fails?
- Verify baseURL is correct
- Check network connectivity
- Ensure backend accepts USDZ format
- Check response format matches AnalysisResult model

## License

This project is provided as-is for the Rhinovate iOS app.

