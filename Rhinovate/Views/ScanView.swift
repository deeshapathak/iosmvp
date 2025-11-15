import SwiftUI
import ARKit

struct ScanView: UIViewControllerRepresentable {
    typealias UIViewControllerType = ARFaceScanViewController
    
    let onFinished: (URL) -> Void
    
    func makeUIViewController(context: Context) -> ARFaceScanViewController {
        let vc = ARFaceScanViewController()
        vc.onFinished = onFinished
        return vc
    }
    
    func updateUIViewController(_ uiViewController: ARFaceScanViewController, context: Context) {}
}
