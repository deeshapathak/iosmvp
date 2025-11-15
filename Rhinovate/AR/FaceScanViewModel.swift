import Foundation
import ARKit
import Combine

@MainActor
final class FaceScanViewModel: NSObject, ObservableObject, ARSessionDelegate {
    enum State: Equatable {
        case idle
        case scanning
        case uploading
        case success(UploadResponse)
        case error(String)
    }
    
    @Published var state: State = .idle
    @Published var instructionText: String = "Slowly turn your head left and right."
    
    let session = ARSession()
    private var latestFaceGeometry: ARFaceGeometry?
    private let apiClient: APIClient
    
    init(apiClient: APIClient) {
        self.apiClient = apiClient
        super.init()
        session.delegate = self
    }
    
    convenience override init() {
        self.init(apiClient: .shared)
    }
    
    func startScanning() {
        guard ARFaceTrackingConfiguration.isSupported else {
            state = .error("This device does not support Face Tracking.")
            return
        }
        let config = ARFaceTrackingConfiguration()
        config.isLightEstimationEnabled = true
        // TODO: Consider additional configuration if needed
        session.run(config, options: [.resetTracking, .removeExistingAnchors])
        state = .scanning
    }
    
    func stopScanning() {
        session.pause()
    }
    
    func finishAndUpload(patientId: String) async {
        guard case .scanning = state, let geometry = latestFaceGeometry else {
            state = .error("No face mesh captured yet. Please try again.")
            return
        }
        do {
            let fileURL = try FaceScanExporter.exportOBJ(from: geometry)
            state = .uploading
            let response = try await apiClient.uploadFaceScan(fileURL: fileURL, patientId: patientId)
            state = .success(response)
        } catch {
            state = .error(error.localizedDescription)
        }
    }
    
    // MARK: - ARSessionDelegate
    func session(_ session: ARSession, didUpdate anchors: [ARAnchor]) {
        guard case .scanning = state else { return }
        if let faceAnchor = anchors.compactMap({ $0 as? ARFaceAnchor }).first {
            // Keep latest geometry
            latestFaceGeometry = faceAnchor.geometry
        }
    }
    
    func session(_ session: ARSession, cameraDidChangeTrackingState camera: ARCamera) {
        switch camera.trackingState {
        case .notAvailable:
            instructionText = "Tracking not available."
        case .limited(let reason):
            switch reason {
            case .excessiveMotion: instructionText = "Hold still."
            case .insufficientFeatures: instructionText = "Move to a well-lit area."
            case .initializing, .relocalizing: instructionText = "Initializing…"
            @unknown default: instructionText = "Limited tracking."
            }
        case .normal:
            instructionText = "Slowly turn your head left and right."
        }
    }
}

