import UIKit
import ARKit
import SceneKit

class ARFaceScanViewController: UIViewController, ARSessionDelegate {
    var onFinished: ((URL) -> Void)?
    private let session = ARSession()
    private var hasExported = false
    private var sceneView: ARSCNView!
    private var faceNode: SCNNode?
    private var captureButton: UIButton!
    private var statusLabel: UILabel!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        sceneView = ARSCNView(frame: view.bounds)
        view.addSubview(sceneView)
        
        sceneView.session = session
        sceneView.automaticallyUpdatesLighting = true
        
        // close button
        let closeButton = UIButton(type: .system)
        closeButton.setTitle("Cancel", for: .normal)
        closeButton.addTarget(self, action: #selector(closeTapped), for: .touchUpInside)
        closeButton.frame = CGRect(x: 20, y: 50, width: 80, height: 40)
        closeButton.backgroundColor = UIColor.systemBackground.withAlphaComponent(0.8)
        closeButton.layer.cornerRadius = 8
        view.addSubview(closeButton)
        
        // status label
        statusLabel = UILabel()
        statusLabel.text = "Position your face in view"
        statusLabel.textColor = .white
        statusLabel.textAlignment = .center
        statusLabel.backgroundColor = UIColor.black.withAlphaComponent(0.6)
        statusLabel.layer.cornerRadius = 8
        statusLabel.clipsToBounds = true
        statusLabel.numberOfLines = 0
        statusLabel.frame = CGRect(x: 20, y: view.bounds.height - 200, width: view.bounds.width - 40, height: 60)
        statusLabel.font = UIFont.systemFont(ofSize: 16, weight: .medium)
        view.addSubview(statusLabel)
        
        // capture button
        captureButton = UIButton(type: .system)
        captureButton.setTitle("Capture", for: .normal)
        captureButton.addTarget(self, action: #selector(captureTapped), for: .touchUpInside)
        captureButton.frame = CGRect(x: view.bounds.width / 2 - 60, y: view.bounds.height - 100, width: 120, height: 50)
        captureButton.backgroundColor = UIColor.systemGray
        captureButton.setTitleColor(.white, for: .normal)
        captureButton.layer.cornerRadius = 25
        captureButton.isEnabled = false
        view.addSubview(captureButton)
        
        let configuration = ARFaceTrackingConfiguration()
        configuration.isLightEstimationEnabled = true
        session.delegate = self
        session.run(configuration, options: [.resetTracking, .removeExistingAnchors])
    }
    
    @objc func closeTapped() {
        session.pause()
        dismiss(animated: true)
    }
    
    @objc func captureTapped() {
        guard !hasExported else { return }
        guard let faceNode = faceNode else {
            statusLabel.text = "Face not detected. Please try again."
            return
        }
        
        statusLabel.text = "Capturing..."
        captureButton.isEnabled = false
        export(node: faceNode)
    }
    
    func session(_ session: ARSession, didUpdate anchors: [ARAnchor]) {
        guard !hasExported else { return }
        guard let faceAnchor = anchors.first as? ARFaceAnchor else {
            DispatchQueue.main.async {
                self.statusLabel.text = "Position your face in view"
                self.captureButton.backgroundColor = UIColor.systemGray
                self.captureButton.isEnabled = false
            }
            return
        }
        guard let device = sceneView.device else { return }
        
        // build face geometry from anchor
        if faceNode == nil {
            let faceGeometry = ARSCNFaceGeometry(device: device)!
            faceNode = SCNNode(geometry: faceGeometry)
            sceneView.scene.rootNode.addChildNode(faceNode!)
        }
        
        if let faceNode = faceNode, let geometry = faceNode.geometry as? ARSCNFaceGeometry {
            geometry.update(from: faceAnchor.geometry)
        }
        
        // Update UI when face is detected
        DispatchQueue.main.async {
            self.statusLabel.text = "Face detected! Ready to capture."
            self.captureButton.backgroundColor = UIColor.systemBlue
            self.captureButton.isEnabled = true
        }
    }
    
    private func export(node: SCNNode) {
        hasExported = true
        session.pause()
        
        let scene = SCNScene()
        let exportedNode = node.clone()
        scene.rootNode.addChildNode(exportedNode)
        
        let url = FileManager.default.temporaryDirectory.appendingPathComponent("face_\(UUID().uuidString).usdz")
        
        scene.write(to: url, options: nil, delegate: nil, progressHandler: nil)
        // If the file exists at the URL after writing, treat as success; otherwise, use fallback.
        if FileManager.default.fileExists(atPath: url.path) {
            DispatchQueue.main.async {
                self.onFinished?(url)
                self.dismiss(animated: true)
            }
        } else {
            // Fallback: try using alternate export path
            DispatchQueue.main.async {
                self.exportFallback(scene: scene, url: url)
            }
        }
    }
    
    private func exportFallback(scene: SCNScene, url: URL) {
        // Alternative export method using intermediate .scn file copy
        let tempURL = FileManager.default.temporaryDirectory.appendingPathComponent("temp.scn")
        scene.write(to: tempURL, options: nil, delegate: nil, progressHandler: nil)

        if FileManager.default.fileExists(atPath: tempURL.path) {
            // Attempt to copy the file; handle potential existing file by removing first
            try? FileManager.default.removeItem(at: url)
            do {
                try FileManager.default.copyItem(at: tempURL, to: url)
                self.onFinished?(url)
                self.dismiss(animated: true)
                return
            } catch {
                print("Fallback export copy failed: \(error)")
            }
        }

        // If all else fails, dismiss anyway
        self.dismiss(animated: true)
    }
}

