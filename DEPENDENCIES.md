# 📦 Complete Dependencies List

All dependencies needed to run the Rhinovate iOS app with 3D face scanning and API integration.

## 🍎 iOS App Dependencies

### Required Frameworks (Built into iOS - No Installation Needed)

These are Apple frameworks that come with iOS. Just make sure they're linked in Xcode:

1. **SwiftUI** ✅
   - Native UI framework
   - Used for: HomeView, ScanView, ResultView
   - **Auto-linked** - No action needed

2. **ARKit** ✅
   - Augmented Reality framework
   - Used for: Face tracking, 3D mesh capture
   - **Auto-linked** - No action needed
   - **Requires**: iPhone with Face ID (iPhone X or newer)

3. **SceneKit** ✅
   - 3D graphics framework
   - Used for: Rendering face mesh, exporting to USDZ
   - **Auto-linked** - No action needed

4. **Foundation** ✅
   - Core framework
   - Used for: URLSession, networking, file I/O
   - **Auto-linked** - No action needed

### Xcode Project Requirements

1. **Xcode** (Latest version recommended)
   - Download from App Store or Apple Developer
   - Minimum: Xcode 14.0+ (for iOS 13.0+ support)

2. **iOS Deployment Target**
   - Set to **iOS 13.0** or later
   - Required for ARKit face tracking

3. **Swift Version**
   - Swift 5.0 or later
   - Auto-configured in Xcode

### Device Requirements

- **Physical iPhone** (not simulator)
- **iPhone X or newer** (has TrueDepth camera/Face ID)
- **iOS 13.0 or later**

### Permissions (Info.plist)

Add these to your `Info.plist` or Xcode Target → Info:

```xml
<key>NSCameraUsageDescription</key>
<string>We need camera access to scan your face for AI analysis.</string>

<key>NSFaceIDUsageDescription</key>
<string>Face tracking is used to capture a 3D model of your face.</string>
```

### No External Libraries Needed! 🎉

The iOS app uses **only Apple frameworks** - no CocoaPods, Swift Package Manager, or third-party libraries required.

---

## 🐍 Backend API Dependencies

### Python Requirements

Install these Python packages:

```bash
pip install -r requirements.txt
```

### Python Packages (from requirements.txt)

1. **fastapi** 📡
   - Modern web framework
   - Used for: REST API endpoints
   - Version: Latest

2. **uvicorn[standard]** 🚀
   - ASGI server
   - Used for: Running the FastAPI server
   - Version: Latest with standard extras

3. **python-multipart** 📎
   - Multipart form data parser
   - Used for: File upload handling
   - Version: Latest

4. **pydantic** ✅
   - Data validation
   - Used for: Request/response models
   - Version: Latest

5. **pydantic-settings** ⚙️
   - Settings management
   - Used for: Configuration (UPLOAD_DIR, etc.)
   - Version: Latest

6. **trimesh** 🔷
   - 3D mesh processing
   - Used for: Parsing USDZ/OBJ/GLB files
   - Version: Latest

7. **numpy** 🔢
   - Numerical computing
   - Used for: Landmark calculations, array operations
   - Version: Latest

8. **scipy** 🔬
   - Scientific computing
   - Used for: Distance calculations, spatial operations
   - Version: Latest

### Python Version

- **Python 3.7 or later**
- Recommended: Python 3.9+

### System Requirements (Backend)

- **macOS, Linux, or Windows**
- **Internet connection** (for initial pip install)
- **Disk space**: ~500MB for dependencies + uploads

---

## 🔧 Installation Steps

### iOS App Setup

1. **Open Xcode**
2. **Create/Open project**
3. **Link frameworks** (usually auto-linked):
   - Target → General → Frameworks, Libraries, and Embedded Content
   - Verify: SwiftUI, ARKit, SceneKit, Foundation are present
4. **Set deployment target**: iOS 13.0+
5. **Add permissions** to Info.plist
6. **Build** (⌘B)

**No package managers needed!**

### Backend Setup

```bash
# 1. Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📋 Quick Checklist

### iOS App ✅
- [ ] Xcode installed
- [ ] Project created with SwiftUI
- [ ] Deployment target: iOS 13.0+
- [ ] ARKit framework linked (auto)
- [ ] SceneKit framework linked (auto)
- [ ] Camera permission added
- [ ] Face ID permission added
- [ ] Physical iPhone connected

### Backend ✅
- [ ] Python 3.7+ installed
- [ ] Virtual environment created (optional)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Server running (`uvicorn app.main:app --reload`)

---

## 🚫 What You DON'T Need

### iOS App
- ❌ CocoaPods
- ❌ Swift Package Manager packages
- ❌ Carthage
- ❌ Third-party libraries
- ❌ External dependencies

### Backend
- ❌ Database (uses JSON file for metadata)
- ❌ Redis
- ❌ Celery
- ❌ Docker (optional, not required)
- ❌ Cloud services (can run locally)

---

## 🔍 Verify Dependencies

### Check iOS Frameworks

In Xcode:
1. Select project → Target → General
2. Scroll to "Frameworks, Libraries, and Embedded Content"
3. Should see: SwiftUI, ARKit, SceneKit, Foundation

### Check Python Packages

```bash
pip list | grep -E "(fastapi|uvicorn|trimesh|numpy|scipy)"
```

Should show all packages installed.

### Test Backend

```bash
# Start server
uvicorn app.main:app --reload

# In another terminal, test
curl http://127.0.0.1:8000/
# Should return: {"status":"ok","service":"rhinovate",...}
```

---

## 📱 Complete System Architecture

```
iOS App (Swift/SwiftUI)
├── Frameworks: SwiftUI, ARKit, SceneKit, Foundation
├── No external dependencies
└── Connects to: Backend API

Backend API (Python/FastAPI)
├── fastapi (web framework)
├── uvicorn (server)
├── trimesh (3D processing)
├── numpy/scipy (calculations)
└── pydantic (validation)
```

---

## 🎯 Summary

**iOS App:**
- ✅ Zero external dependencies
- ✅ Uses only Apple frameworks
- ✅ No package managers needed

**Backend:**
- ✅ 8 Python packages
- ✅ Install with: `pip install -r requirements.txt`
- ✅ All open-source, well-maintained

**Total setup time:** ~5 minutes for backend, iOS app is ready to build!

