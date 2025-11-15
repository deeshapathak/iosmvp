import SwiftUI

@main
struct RhinovatePatientScanApp: App {
    @State private var appState: AppState = .welcome
    @State private var lastUploadResponse: UploadResponse?
    
    var body: some Scene {
        WindowGroup {
            NavigationStack {
                switch appState {
                case .welcome:
                    WelcomeView {
                        appState = .scanning
                    }
                case .scanning:
                    FaceScanView(patientId: "patient_demo_001") { result in
                        switch result {
                        case .success(let response):
                            lastUploadResponse = response
                            appState = .success
                        case .failure(let error):
                            appState = .error(error.localizedDescription)
                        }
                    }
                case .success:
                    SuccessView(response: lastUploadResponse) {
                        appState = .welcome
                    }
                case .error(let message):
                    ErrorView(message: message) {
                        appState = .welcome
                    }
                }
            }
        }
    }
}

// MARK: - App State

enum AppState: Equatable {
    case welcome
    case scanning
    case success
    case error(String)
}

// MARK: - Simple Screens

struct WelcomeView: View {
    var onStart: () -> Void
    
    var body: some View {
        VStack(spacing: 24) {
            Spacer()
            Text("Rhinovate")
                .font(.largeTitle).bold()
            Text("3D Face Scan for Surgical Planning")
                .font(.subheadline)
                .foregroundStyle(.secondary)
            Spacer()
            Button(action: onStart) {
                Text("Start Face Scan")
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.accentColor)
                    .foregroundStyle(.white)
                    .clipShape(RoundedRectangle(cornerRadius: 12))
            }
            .padding(.horizontal)
            Spacer(minLength: 40)
        }
    }
}

struct SuccessView: View {
    let response: UploadResponse?
    var onDone: () -> Void
    
    var body: some View {
        VStack(spacing: 16) {
            Spacer()
            Image(systemName: "checkmark.seal.fill")
                .font(.system(size: 64))
                .foregroundStyle(.green)
            Text("Face scan uploaded successfully.")
                .font(.title3).bold()
            if let response { 
                Text("ID: \(response.id)")
                    .font(.footnote)
                    .foregroundStyle(.secondary)
            }
            Spacer()
            Button("Done", action: onDone)
                .buttonStyle(.borderedProminent)
            Spacer(minLength: 40)
        }
        .padding()
    }
}

struct ErrorView: View {
    let message: String
    var onDismiss: () -> Void
    
    var body: some View {
        VStack(spacing: 16) {
            Spacer()
            Image(systemName: "exclamationmark.triangle.fill")
                .font(.system(size: 64))
                .foregroundStyle(.yellow)
            Text("Upload Failed")
                .font(.title3).bold()
            Text(message)
                .font(.footnote)
                .multilineTextAlignment(.center)
                .foregroundStyle(.secondary)
            Spacer()
            Button("Back", action: onDismiss)
                .buttonStyle(.borderedProminent)
            Spacer(minLength: 40)
        }
        .padding()
    }
}

#Preview("Welcome") {
    NavigationStack {
        WelcomeView {
            // start action for preview
        }
        .padding()
    }
}

