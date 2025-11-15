# 📁 Xcode Project Structure & Targets

## Targets in Your Project

Your Xcode project has **3 targets**:

### 1. **Rhinovate** (Main App Target) ✅
- **Type**: Application
- **Product**: `Rhinovate.app`
- **Purpose**: Main iOS app
- **Contains**: All app code (Views, Services, Models, AR)

### 2. **RhinovateTests** (Unit Tests) 🧪
- **Type**: Unit Test Bundle
- **Product**: `RhinovateTests.xctest`
- **Purpose**: Unit tests for app logic
- **Dependencies**: Depends on `Rhinovate` target
- **Status**: Empty (no tests written yet)

### 3. **RhinovateUITests** (UI Tests) 🎨
- **Type**: UI Test Bundle
- **Product**: `RhinovateUITests.xctest`
- **Purpose**: UI automation tests
- **Dependencies**: Depends on `Rhinovate` target
- **Status**: Empty (no tests written yet)

## Frameworks & Dependencies

### ✅ System Frameworks (Auto-Linked)
These are Apple frameworks that are **automatically linked** - no configuration needed:

- **SwiftUI** - UI framework
- **ARKit** - Face tracking
- **SceneKit** - 3D rendering
- **Foundation** - Core functionality

**No manual linking required!** Xcode handles this automatically.

### ❌ No Local Frameworks
- No custom frameworks defined
- No `.framework` bundles in the project
- No framework targets

### ❌ No Swift Package Dependencies
- No Swift Package Manager packages
- `packageProductDependencies` is empty
- No external Swift packages

### ❌ No CocoaPods
- No Podfile
- No Pods directory
- No CocoaPods integration

## Project Groups (Folders)

Your project is organized into these groups:

```
Rhinovate/
├── AR/                    # ARKit face scanning
│   └── FaceScanViewController.swift
├── Models/                # Data models
│   └── AnalysisResult.swift
├── Services/              # API client
│   └── APIClient.swift
├── Views/                 # SwiftUI views
│   ├── HomeView.swift
│   ├── ScanView.swift
│   └── ResultView.swift
├── Rhinovate/             # Main app folder
│   ├── RhinovateApp.swift
│   └── Assets.xcassets/
├── RhinovateTests/        # Unit tests (empty)
└── RhinovateUITests/      # UI tests (empty)
```

## Build Configuration

### Main App Target Settings
- **Deployment Target**: iOS 26.1 (⚠️ This seems wrong - should be iOS 13.0+)
- **Swift Version**: Auto (should be Swift 5.0+)
- **Build System**: New Build System
- **Frameworks**: Auto-linked (no manual entries)

### Test Targets
- Both test targets depend on the main `Rhinovate` target
- Can access `Models` folder (shared)
- Currently empty (no test code)

## ⚠️ Issues Found

### 1. Deployment Target Too High
Your project shows `IPHONEOS_DEPLOYMENT_TARGET = 26.1` which is incorrect.

**Fix:**
1. Select project → Target "Rhinovate"
2. General → Deployment Info
3. Set to **iOS 13.0** (minimum for ARKit face tracking)

### 2. Duplicate Files
There appear to be duplicate files in the AR folder:
- `Rhinovate/AR/` has multiple files
- Some files might be duplicated

**Check:**
- Make sure each file is only added once
- Remove any duplicate entries

## Summary

✅ **What You Have:**
- 1 main app target
- 2 test targets (empty)
- 4 system frameworks (auto-linked)
- No external dependencies

❌ **What You DON'T Have:**
- No local/custom frameworks
- No helper targets
- No Swift Package dependencies
- No CocoaPods
- No additional modules

## Recommendation

Your project structure is **simple and clean** - exactly what you need! No additional frameworks or targets required. The system frameworks (SwiftUI, ARKit, SceneKit, Foundation) are all you need.

**Just fix the deployment target** to iOS 13.0+ and you're good to go!

