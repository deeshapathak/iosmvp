# Xcode Project Setup Guide

Since this is a Swift package structure, you'll need to create an Xcode project to build and run the app. Here's how:

## Option 1: Create New Xcode Project (Recommended)

1. Open Xcode
2. Create a new project:
   - Choose "iOS" → "App"
   - Product Name: `RhinovateApp`
   - Interface: `SwiftUI`
   - Language: `Swift`
   - Minimum Deployment: `iOS 13.0` (for ARKit face tracking)

3. Replace the default `ContentView.swift` with the files from this repository:
   - Delete the default `ContentView.swift` and `AppNameApp.swift` files
   - Add all folders and files from this repository to your Xcode project
   - Make sure to check "Copy items if needed" if copying

4. Update the app entry point:
   - In Xcode, select your project in the navigator
   - Go to "Build Settings"
   - Search for "Info.plist"
   - Make sure your Info.plist is included

5. Configure capabilities:
   - Select your project target
   - Go to "Signing & Capabilities"
   - Ensure "AR" capability is enabled (if required by your deployment target)

## Option 2: Use Swift Package (Alternative)

If you want to keep the Swift Package structure, you can:

1. Create a new Xcode project
2. Add this directory as a local Swift package dependency
3. Import the modules in your app target

However, for an app project, Option 1 is simpler.

## Important Configuration

### Info.plist
The `Info.plist` file needs to be added to your Xcode project:
- Right-click on your project in Xcode
- Add Files to "[Project Name]"
- Select `Info.plist`
- Make sure it's added to your app target

Alternatively, in newer Xcode projects, you can add the privacy descriptions directly in the target settings:
- Target → Info → Custom iOS Target Properties
- Add `Privacy - Camera Usage Description`
- Add `Privacy - Face ID Usage Description`

### Build Settings
- Ensure Swift version is 5.0+
- Deployment target: iOS 13.0 or later
- Framework search paths should include ARKit and SceneKit

### Required Frameworks
The project uses these frameworks (they should be automatically linked):
- SwiftUI
- ARKit
- SceneKit
- Foundation

## Testing on Device

ARKit face tracking requires:
- A physical iOS device (not simulator)
- iPhone with Face ID (iPhone X or newer)
- iOS 13.0 or later

The simulator does not support ARKit face tracking.

## Troubleshooting

### "Cannot find 'ARSCNFaceGeometry' in scope"
- Make sure ARKit.framework is linked in your target's "Frameworks, Libraries, and Embedded Content"
- Check that your deployment target is iOS 13.0+

### "Info.plist not found"
- Make sure Info.plist is added to your target
- Or configure privacy descriptions directly in target settings

### AR Session fails to start
- Check that camera permissions are granted
- Ensure testing on a physical device with Face ID
- Verify device supports ARKit (iPhone X or newer)

