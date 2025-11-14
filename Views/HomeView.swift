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
                ScanView { fileURL in
                    // when scan is done, call backend
                    isPresentingScan = false
                    isUploading = true
                    errorMessage = nil
                    
                    Task {
                        do {
                            let result = try await APIClient.shared.uploadScan(fileURL: fileURL)
                            await MainActor.run {
                                analysisResult = result
                                isUploading = false
                            }
                        } catch {
                            await MainActor.run {
                                errorMessage = "Upload failed: \(error.localizedDescription)"
                                isUploading = false
                            }
                        }
                    }
                }
            }
        }
    }
}

