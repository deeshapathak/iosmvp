import SwiftUI
import ARKit

struct ScanView: UIViewControllerRepresentable {
    let onFinished: (URL) -> Void
    
    func makeUIViewController(context: Context) -> FaceScanViewController {
        let vc = FaceScanViewController()
        vc.onFinished = onFinished
        return vc
    }
    
    func updateUIViewController(_ uiViewController: FaceScanViewController, context: Context) {}
}

