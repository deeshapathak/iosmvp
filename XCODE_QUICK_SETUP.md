# 🚀 Quick Xcode Setup - Step by Step

Follow these steps to get your iOS app running in Xcode:

## Step 1: Create New Xcode Project

1. **Open Xcode** (should be opening now)
2. **File → New → Project** (or ⌘⇧N)
3. Select **"iOS"** tab → **"App"** → Click **Next**
4. Fill in:
   - **Product Name**: `RhinovateApp`
   - **Team**: Select your Apple Developer account (or "None" for now)
   - **Organization Identifier**: `com.rhinovate` (or your domain)
   - **Bundle Identifier**: Will auto-fill
   - **Interface**: **SwiftUI** ⚠️ (IMPORTANT!)
   - **Language**: **Swift**
   - **Storage**: None (or Core Data if you want it later)
   - **Include Tests**: Optional
5. Click **Next**
6. **Save location**: Choose `/Users/deeshapathak/Desktop/iosmvp/` or create a subfolder
7. Click **Create**

## Step 2: Add Your Files

1. **Delete default files**:
   - In Xcode navigator, find and delete:
     - `ContentView.swift`
     - `RhinovateAppApp.swift` (or similar)

2. **Add your files**:
   - Right-click on the **blue project icon** (top of navigator)
   - Select **"Add Files to 'RhinovateApp'..."**
   - Navigate to `/Users/deeshapathak/Desktop/iosmvp/`
   - Select these items:
     - ✅ `RhinovateApp.swift`
     - ✅ `Models/` folder
     - ✅ `Services/` folder
     - ✅ `Views/` folder
     - ✅ `AR/` folder
     - ✅ `Info.plist`
   - **IMPORTANT**: Check these boxes:
     - ✅ **"Copy items if needed"**
     - ✅ **"Create groups"** (not folder references)
     - ✅ **"Add to targets: RhinovateApp"**
   - Click **Add**

## Step 3: Configure Project Settings

1. **Select the project** (blue icon) in navigator
2. **Select "RhinovateApp" target** (under TARGETS)
3. **General Tab**:
   - **Deployment Info**: Set to **iOS 13.0** (minimum)
   - **Device Orientation**: Portrait (or all if you want)
   
4. **Signing & Capabilities**:
   - ✅ Check **"Automatically manage signing"**
   - Select your **Team** (or "None" for simulator only)
   
5. **Info Tab**:
   - Verify these keys exist (or add them):
     - `Privacy - Camera Usage Description`: "We need camera access to scan your face for AI analysis."
     - `Privacy - Face ID Usage Description`: "Face tracking is used to capture a 3D model of your face."

6. **Build Settings**:
   - Search for "Swift Language Version"
   - Set to **Swift 5** (or latest)

## Step 4: Update API URL (For Testing)

1. Open `Services/APIClient.swift` in Xcode
2. Find line 8:
   ```swift
   private let baseURL = URL(string: "https://api.rhinovate.ai")!
   ```
3. Change to your local backend:
   ```swift
   private let baseURL = URL(string: "http://127.0.0.1:8000")!  // For simulator
   // OR for physical device:
   // private let baseURL = URL(string: "http://YOUR_MAC_IP:8000")!
   ```

## Step 5: Build and Run

1. **Connect a physical iPhone** (ARKit doesn't work in simulator)
   - Must be iPhone X or newer (has Face ID)
   - Unlock and trust the computer if prompted

2. **Select your device** in the device selector (top toolbar)

3. **Build and Run**: Press **⌘R** or click the Play button

4. **First time**: You may need to:
   - Trust your developer certificate on the device
   - Settings → General → VPN & Device Management → Trust

## Step 6: Test the App

1. **Start the backend server first**:
   ```bash
   cd /Users/deeshapathak/Desktop/iosmvp
   python3 -m pip install -r requirements.txt
   python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **In the iOS app**:
   - Tap "Scan my face"
   - Grant camera permission when prompted
   - Position your face in view
   - Wait for "Face detected! Ready to capture."
   - Tap "Capture"
   - Wait for upload and results

## Troubleshooting

### "Cannot find 'ARSCNFaceGeometry' in scope"
- Make sure ARKit framework is linked:
  - Target → General → Frameworks, Libraries, and Embedded Content
  - Add `ARKit.framework` if missing

### "Info.plist not found"
- The Info.plist should be in your project
- Or add the privacy keys directly in Target → Info tab

### ARKit not working
- ⚠️ **Must use physical device** (not simulator)
- Must be iPhone X or newer
- Check camera permissions in Settings

### Can't connect to backend
- Make sure backend is running: `curl http://127.0.0.1:8000/`
- For physical device, use Mac's IP address (not 127.0.0.1)
- Find Mac IP: `ifconfig | grep "inet " | grep -v 127.0.0.1`

### Build errors
- Clean build folder: **⌘⇧K**
- Delete DerivedData: **⌘⇧⌥K**
- Restart Xcode

## ✅ You're Done!

Your app should now work. The landmark extraction will happen automatically on the backend when you upload a scan.

