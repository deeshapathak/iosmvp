# Landmark Extraction from 3D Models

This document describes the implementation of facial landmark extraction from 3D mesh files (USDZ, OBJ, GLB).

## Overview

The landmark extraction system processes 3D face scans uploaded from the iOS app and extracts key facial landmarks using geometric methods. These landmarks are then used to compute facial measurements for cosmetic analysis.

## Implementation

### Files

- `app/services/landmark_extractor.py` - Core landmark extraction logic
- `app/services/storage.py` - Updated to use landmark extraction
- `app/services/facial_analysis.py` - Updated to compute real measurements from landmarks

### Supported Formats

1. **USDZ** - Apple's Universal Scene Description format (zip archive)
   - Extracts OBJ/GLB files from the archive
   - Falls back to direct mesh loading if needed

2. **OBJ** - Wavefront OBJ format
   - Direct parsing using trimesh

3. **GLB/GLTF** - glTF binary/text format
   - Handles scene objects and extracts first mesh

### Landmark Detection Method

The system uses **geometric landmark detection** based on:

1. **Extreme Points**: 
   - Nose tip: Most forward point (max Z)
   - Chin: Lowest point (min Y)
   - Forehead: Highest point in upper region (max Y)

2. **Regional Analysis**:
   - Eye regions: Points in upper-middle area, split by left/right
   - Mouth corners: Points in lower-middle area, split by left/right

3. **Symmetry Assumptions**:
   - Face is assumed to be roughly centered
   - Left/right regions determined by X coordinate relative to center

### Extracted Landmarks

The system extracts the following landmarks:

- `nose_tip` - Tip of the nose
- `chin` - Lowest point on chin
- `forehead_center` - Center of forehead
- `left_eye_outer` / `right_eye_outer` - Outer eye corners
- `left_eye_inner` / `right_eye_inner` - Inner eye corners
- `mouth_left` / `mouth_right` - Mouth corners
- `mouth_center` - Center of mouth

### Measurements Computed

From the extracted landmarks, the system computes:

1. **Inter-Pupillary Distance (IPD)** - Distance between eyes
2. **Nose-to-IPD Ratio** - Nose width relative to eye distance
3. **Chin Projection** - Forward projection of chin (in mm)
4. **Jawline Asymmetry** - Measure of facial asymmetry (in mm)
5. **Face Height** - Vertical distance from chin to forehead (optional)

## Usage

The landmark extraction is automatically called when a 3D scan is uploaded:

```python
# In storage.py
landmarks = extract_landmarks_from_mesh(dest_path)
result = analyze_landmarks(landmarks)
```

## Dependencies

New dependencies added to `requirements.txt`:

- `trimesh` - 3D mesh processing
- `numpy` - Numerical computations
- `scipy` - Scientific computing (for distance calculations)

## Limitations & Future Improvements

### Current Limitations

1. **Geometric Method**: Uses simple geometric heuristics, not ML-based detection
2. **Orientation Assumptions**: Assumes face-forward orientation (Z forward, Y up)
3. **No ARKit Topology**: Doesn't leverage ARKit's known face mesh topology
4. **USDZ Parsing**: Basic USDZ support (extracts OBJ/GLB from zip)

### Future Enhancements

1. **ARKit Topology Mapping**: 
   - ARKit provides ~1220 vertices in a known order
   - Could map specific vertex indices to landmarks

2. **ML-Based Detection**:
   - Train a model on 3D face meshes with labeled landmarks
   - More accurate than geometric methods

3. **Curvature Analysis**:
   - Use surface curvature to identify landmarks (nose tip, eye sockets)
   - More robust to orientation variations

4. **MediaPipe Integration**:
   - Render mesh to 2D image
   - Use MediaPipe Face Mesh for landmark detection
   - Project back to 3D

5. **USD/USDZ Native Support**:
   - Use `pxr` (Pixar USD) library for native USD parsing
   - Better handling of USDZ files

## Testing

To test the landmark extraction:

```bash
# Start the backend
uvicorn app.main:app --reload

# Upload a 3D scan
curl -X POST http://127.0.0.1:8000/analyze-scan \
  -F "file=@test_face.usdz"
```

The response will include analysis based on extracted landmarks instead of placeholders.

## Error Handling

The system includes fallback mechanisms:

- If landmark extraction fails, uses placeholder landmarks
- Logs warnings but continues processing
- Ensures API always returns a valid response

This ensures the iOS app continues to work even if landmark extraction encounters issues.

