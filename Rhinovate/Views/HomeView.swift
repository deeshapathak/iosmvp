import SwiftUI

struct HomeView: View {
    @State private var isPresentingScan = false
    @State private var analysisResult: AnalysisResult?
    @State private var isUploading = false
    @State private var errorMessage: String?
    
    var body: some View {
        NavigationStack {
            VStack(spacing: 24) {
                Text("Rhinovate AI")
                    .font(.largeTitle.bold())
                
                Text("Scan your face to see AI-enhanced cosmetic suggestions.")
                    .multilineTextAlignment(.center)
                    .foregroundColor(.secondary)
                
                Button {
                    isPresentingScan = true
                } label: {
                    Text("Scan my face")
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(14)
                }
                .disabled(isUploading)
                
                if isUploading {
                    ProgressView("Uploading scan...")
                        .padding()
                }
                
                if let errorMessage = errorMessage {
                    Text(errorMessage)
                        .foregroundColor(.red)
                        .font(.caption)
                        .padding()
                }
            }
            .padding()
            .navigationDestination(item: $analysisResult) { result in
                ResultView(result: result)
            }
            .sheet(isPresented: $isPresentingScan) {
                NavigationStack {
                    FaceScanView(patientId: "home_patient_demo") { result in
                        // On completion from ARKit-based scan flow
                        isPresentingScan = false
                        switch result {
                        case .success(let response):
                            // Map UploadResponse to AnalysisResult for navigation
                            if let analysis = mapUploadResponseToAnalysis(response) {
                                errorMessage = nil
                                analysisResult = analysis
                            } else {
                                errorMessage = "Couldn't interpret server response. Please try again."
                            }
                        case .failure(let error):
                            errorMessage = "Upload failed: \(error.localizedDescription)"
                        }
                    }
                }
            }
        }
    }
}

fileprivate extension HomeView {
    /// Convert the server's upload response into an AnalysisResult used for navigation.
    /// Replace the implementation with real field mapping once available.
    func mapUploadResponseToAnalysis(_ response: UploadResponse) -> AnalysisResult? {
        // TODO: Map fields from UploadResponse to AnalysisResult.
        // For example, if `UploadResponse` contains an `analysis` property:
        // return response.analysis
        // Or construct one:
        // return AnalysisResult(id: response.id, suggestions: response.suggestions, ...)
        return nil
    }
}
