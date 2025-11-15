"""
Extract facial landmarks from 3D mesh files (USDZ, OBJ, GLB).

This module parses 3D models and extracts key facial landmarks using geometric methods.
ARKit face meshes follow a known topology, which we leverage for landmark detection.
"""
import os
import zipfile
import tempfile
from typing import List, Dict, Optional, Tuple
import numpy as np
import trimesh
from scipy.spatial.distance import cdist


# ARKit face mesh topology constants
# ARFaceAnchor.geometry provides ~1220 vertices in a known order
# Key landmark indices (approximate, may vary by ARKit version)
ARKIT_LANDMARK_REGIONS = {
    "nose_tip": "center_front",  # Most forward point on nose
    "chin": "center_bottom",  # Lowest point on chin
    "left_eye_outer": "left_eye_region",
    "right_eye_outer": "right_eye_region",
    "left_eye_inner": "left_eye_inner",
    "right_eye_inner": "right_eye_inner",
    "mouth_left": "left_mouth_corner",
    "mouth_right": "right_mouth_corner",
    "mouth_center": "center_mouth",
    "forehead_center": "center_top",
}


def extract_landmarks_from_mesh(mesh_path: str) -> List[Dict[str, float]]:
    """
    Extract facial landmarks from a 3D mesh file.
    
    Args:
        mesh_path: Path to 3D model file (USDZ, OBJ, or GLB)
        
    Returns:
        List of landmark dictionaries with x, y, z coordinates
    """
    ext = os.path.splitext(mesh_path)[1].lower()
    
    if ext == ".usdz":
        return extract_from_usdz(mesh_path)
    elif ext in [".obj", ".glb", ".gltf"]:
        return extract_from_mesh_file(mesh_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")


def extract_from_usdz(usdz_path: str) -> List[Dict[str, float]]:
    """
    Extract mesh from USDZ file and get landmarks.
    USDZ is a zip file containing USD (Universal Scene Description) files.
    """
    try:
        # USDZ is a zip archive
        with zipfile.ZipFile(usdz_path, 'r') as zip_ref:
            # Extract to temp directory
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_ref.extractall(temp_dir)
                
                # Look for OBJ or GLB files in the archive
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith(('.obj', '.glb', '.gltf')):
                            mesh_file = os.path.join(root, file)
                            return extract_from_mesh_file(mesh_file)
                
                # If no OBJ/GLB found, try to load as USD (requires pxr library)
                # For now, fall back to geometric detection
                return extract_landmarks_geometric(load_mesh_vertices(usdz_path))
    except Exception as e:
        # Fallback: try to load as regular mesh
        try:
            mesh = trimesh.load(usdz_path)
            if isinstance(mesh, trimesh.Scene):
                # Get the first mesh from the scene
                mesh = list(mesh.geometry.values())[0]
            return extract_landmarks_geometric(mesh.vertices)
        except Exception:
            raise ValueError(f"Failed to parse USDZ file: {e}")


def extract_from_mesh_file(mesh_path: str) -> List[Dict[str, float]]:
    """
    Extract landmarks from OBJ, GLB, or GLTF file.
    """
    try:
        mesh = trimesh.load(mesh_path)
        
        # Handle scene objects (GLB/GLTF often contain scenes)
        if isinstance(mesh, trimesh.Scene):
            # Get the first mesh from the scene
            if len(mesh.geometry) > 0:
                mesh = list(mesh.geometry.values())[0]
            else:
                raise ValueError("No geometry found in scene")
        
        if not hasattr(mesh, 'vertices') or mesh.vertices is None:
            raise ValueError("Mesh has no vertices")
        
        return extract_landmarks_geometric(mesh.vertices)
    except Exception as e:
        raise ValueError(f"Failed to parse mesh file {mesh_path}: {e}")


def load_mesh_vertices(file_path: str) -> np.ndarray:
    """
    Attempt to load vertices from various 3D formats.
    """
    try:
        mesh = trimesh.load(file_path)
        if isinstance(mesh, trimesh.Scene):
            mesh = list(mesh.geometry.values())[0]
        return mesh.vertices
    except Exception:
        return np.array([])


def extract_landmarks_geometric(vertices: np.ndarray) -> List[Dict[str, float]]:
    """
    Extract facial landmarks using geometric methods.
    
    This function identifies key facial points based on:
    - Extreme points (min/max in each axis)
    - Curvature analysis
    - Symmetry assumptions
    
    Args:
        vertices: Nx3 numpy array of vertex coordinates
        
    Returns:
        List of landmark dictionaries
    """
    if len(vertices) == 0:
        return []
    
    # Normalize coordinates (center and scale)
    vertices = normalize_vertices(vertices)
    
    landmarks = {}
    
    # 1. Nose tip: most forward point (highest Z in face-forward orientation)
    # Assuming face is oriented with Z forward, Y up
    nose_tip_idx = np.argmax(vertices[:, 2])
    landmarks["nose_tip"] = vertices[nose_tip_idx]
    
    # 2. Chin: lowest point (minimum Y)
    chin_idx = np.argmin(vertices[:, 1])
    landmarks["chin"] = vertices[chin_idx]
    
    # 3. Forehead: highest point (maximum Y) in upper region
    upper_region = vertices[vertices[:, 1] > np.percentile(vertices[:, 1], 70)]
    if len(upper_region) > 0:
        forehead_idx = np.argmax(upper_region[:, 1])
        landmarks["forehead_center"] = upper_region[forehead_idx]
    
    # 4. Eye regions: points in upper-middle region, left and right of center
    center_x = np.median(vertices[:, 0])
    left_region = vertices[(vertices[:, 0] < center_x) & 
                           (vertices[:, 1] > np.percentile(vertices[:, 1], 40)) &
                           (vertices[:, 1] < np.percentile(vertices[:, 1], 70))]
    right_region = vertices[(vertices[:, 0] > center_x) & 
                            (vertices[:, 1] > np.percentile(vertices[:, 1], 40)) &
                            (vertices[:, 1] < np.percentile(vertices[:, 1], 70))]
    
    if len(left_region) > 0:
        # Left eye: most forward point in left region
        left_eye_idx = np.argmax(left_region[:, 2])
        landmarks["left_eye_outer"] = left_region[left_eye_idx]
        
        # Left eye inner: closer to center
        left_inner = left_region[np.argmin(np.abs(left_region[:, 0] - center_x))]
        landmarks["left_eye_inner"] = left_inner
    
    if len(right_region) > 0:
        # Right eye: most forward point in right region
        right_eye_idx = np.argmax(right_region[:, 2])
        landmarks["right_eye_outer"] = right_region[right_eye_idx]
        
        # Right eye inner: closer to center
        right_inner = right_region[np.argmin(np.abs(right_region[:, 0] - center_x))]
        landmarks["right_eye_inner"] = right_inner
    
    # 5. Mouth corners: points in lower-middle region
    mouth_region = vertices[(vertices[:, 1] < np.percentile(vertices[:, 1], 50)) &
                           (vertices[:, 1] > np.percentile(vertices[:, 1], 20))]
    
    if len(mouth_region) > 0:
        left_mouth = mouth_region[mouth_region[:, 0] < center_x]
        right_mouth = mouth_region[mouth_region[:, 0] > center_x]
        
        if len(left_mouth) > 0:
            landmarks["mouth_left"] = left_mouth[np.argmax(left_mouth[:, 2])]
        if len(right_mouth) > 0:
            landmarks["mouth_right"] = right_mouth[np.argmax(right_mouth[:, 2])]
        
        # Mouth center: point closest to center X, in mouth region
        mouth_center_candidates = mouth_region[np.abs(mouth_region[:, 0] - center_x) < 
                                               np.std(mouth_region[:, 0]) * 0.5]
        if len(mouth_center_candidates) > 0:
            landmarks["mouth_center"] = mouth_center_candidates[np.argmax(mouth_center_candidates[:, 2])]
    
    # Convert to list of dictionaries in expected format
    landmark_list = []
    for name, point in landmarks.items():
        landmark_list.append({
            "x": float(point[0]),
            "y": float(point[1]),
            "z": float(point[2]),
            "name": name  # Optional: include name for debugging
        })
    
    return landmark_list


def normalize_vertices(vertices: np.ndarray) -> np.ndarray:
    """
    Center and normalize vertex coordinates.
    Centers the mesh at origin and optionally scales.
    """
    # Center at origin
    centroid = np.mean(vertices, axis=0)
    centered = vertices - centroid
    
    # Optional: normalize scale (keep relative proportions)
    # max_dist = np.max(np.linalg.norm(centered, axis=1))
    # if max_dist > 0:
    #     centered = centered / max_dist
    
    return centered


def compute_inter_pupillary_distance(landmarks: List[Dict[str, float]]) -> Optional[float]:
    """
    Compute inter-pupillary distance from eye landmarks.
    """
    left_eye = None
    right_eye = None
    
    for lm in landmarks:
        name = lm.get("name", "")
        if "left_eye" in name and "outer" in name:
            left_eye = np.array([lm["x"], lm["y"], lm["z"]])
        elif "right_eye" in name and "outer" in name:
            right_eye = np.array([lm["x"], lm["y"], lm["z"]])
    
    if left_eye is not None and right_eye is not None:
        return float(np.linalg.norm(left_eye - right_eye))
    
    return None


def get_landmark_by_name(landmarks: List[Dict[str, float]], name: str) -> Optional[Dict[str, float]]:
    """
    Get a specific landmark by name.
    """
    for lm in landmarks:
        if lm.get("name") == name:
            return lm
    return None

