import Foundation
import ARKit
import SceneKit

/// Helper to export a single ARFaceAnchor geometry to a temporary file.
/// For MVP, we write a very basic OBJ with vertices and triangle indices.
/// - Note: This is a simplified exporter and not production-grade.
struct FaceScanExporter {
    enum ExportError: Error {
        case noGeometry
        case writeFailed
    }
    
    /// Exports the given face anchor geometry as a simple OBJ file in the temporary directory.
    /// - Returns: URL to the written OBJ file.
    static func exportOBJ(from faceGeometry: ARFaceGeometry) throws -> URL {
        // Gather vertices
        let vertices = faceGeometry.vertices
        let indices = faceGeometry.triangleIndices
        
        var obj = "# Rhinovate MVP face mesh\n"
        obj += "o face\n"
        
        // Write vertices: v x y z
        for i in 0..<vertices.count {
            let v = vertices[i]
            obj += String(format: "v %.6f %.6f %.6f\n", v.x, v.y, v.z)
        }
        
        // Faces: OBJ is 1-based index
        // triangleIndices are UInt16 triplets
        for t in stride(from: 0, to: indices.count, by: 3) {
            let i1 = Int(indices[t]) + 1
            let i2 = Int(indices[t+1]) + 1
            let i3 = Int(indices[t+2]) + 1
            obj += "f \(i1) \(i2) \(i3)\n"
        }
        
        let data = obj.data(using: .utf8)!
        let url = FileManager.default.temporaryDirectory.appendingPathComponent("face_\(UUID().uuidString).obj")
        try data.write(to: url)
        return url
    }
}
