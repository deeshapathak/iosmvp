import SwiftUI
import ARKit
import SceneKit

/// SwiftUI wrapper for ARSCNView to display TrueDepth face tracking.
struct FaceScanARView: UIViewRepresentable {
    @ObservedObject var viewModel: FaceScanViewModel
    
    func makeUIView(context: Context) -> ARSCNView {
        let view = ARSCNView(frame: .zero)
        view.automaticallyUpdatesLighting = true
        view.session = viewModel.session
        view.scene = SCNScene()
        return view
    }
    
    func updateUIView(_ uiView: ARSCNView, context: Context) {
        // no-op
    }
}

struct FaceScanView: View {
    let patientId: String
    var onCompleted: (Result<UploadResponse, Error>) -> Void
    
    @StateObject private var viewModel = FaceScanViewModel()
    @State private var showAlert = false
    @State private var alertMessage = ""
    
    var body: some View {
        VStack(spacing: 0) {
            ZStack(alignment: .bottom) {
                FaceScanARView(viewModel: viewModel)
                    .ignoresSafeArea()
                
                VStack(spacing: 12) {
                    Text(viewModel.instructionText)
                        .font(.callout)
                        .foregroundStyle(.white)
                        .padding(8)
                        .background(.black.opacity(0.5))
                        .clipShape(RoundedRectangle(cornerRadius: 8))
                        .padding(.bottom, 8)
                    
                    // Finish & Upload button
                    Button(action: onFinishTapped) {
                        Text(viewModel.state == .uploading ? "Uploading…" : "Finish & Upload")
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(viewModel.state == .uploading ? Color.gray : Color.accentColor)
                            .foregroundStyle(.white)
                            .clipShape(RoundedRectangle(cornerRadius: 12))
                    }
                    .padding(.horizontal)
                    .padding(.bottom, 24)
                    .disabled(!(viewModel.state == .scanning) || viewModel.state == .uploading)
                }
            }
        }
        .task {
            viewModel.startScanning()
        }
        .onChange(of: viewModel.state) { _, newValue in
            switch newValue {
            case .success(let response):
                onCompleted(.success(response))
            case .error(let message):
                alertMessage = message
                showAlert = true
            default:
                break
            }
        }
        .alert("Error", isPresented: $showAlert) {
            Button("OK") { }
        } message: {
            Text(alertMessage)
        }
        .navigationTitle("Face Scan")
        .navigationBarTitleDisplayMode(.inline)
    }
    
    private func onFinishTapped() {
        Task { await viewModel.finishAndUpload(patientId: patientId) }
    }
}

#Preview {
    NavigationStack {
        FaceScanView(patientId: "demo") { _ in }
    }
}
