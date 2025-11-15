import Foundation

struct UploadResponse: Decodable, Equatable {
    let id: String
    let status: String
}

/// Simple API client for uploading face scans.
/// - Note: Uses URLSession with multipart/form-data. No third-party dependencies.
final class APIClient {
    static let shared = APIClient()
    private init() {}
    
    // TODO: Replace with real base URL and auth handling
    private let endpoint = URL(string: "https://api.example.com/face-scan")!
    
    func uploadFaceScan(fileURL: URL, patientId: String) async throws -> UploadResponse {
        var request = URLRequest(url: endpoint)
        request.httpMethod = "POST"
        
        let boundary = "Boundary-\(UUID().uuidString)"
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        
        let body = try await buildMultipartBody(fileURL: fileURL, patientId: patientId, boundary: boundary)
        request.httpBody = body
        
        let (data, response) = try await URLSession.shared.data(for: request)
        guard let http = response as? HTTPURLResponse else {
            throw URLError(.badServerResponse)
        }
        guard 200..<300 ~= http.statusCode else {
            // Attempt to decode error or pass raw message
            let message = String(data: data, encoding: .utf8) ?? "Unknown server error"
            throw NSError(domain: "APIClient", code: http.statusCode, userInfo: [NSLocalizedDescriptionKey: message])
        }
        return try JSONDecoder().decode(UploadResponse.self, from: data)
    }
    
    private func buildMultipartBody(fileURL: URL, patientId: String, boundary: String) async throws -> Data {
        var body = Data()
        let lineBreak = "\r\n"
        
        func appendField(name: String, value: String) {
            body.append("--\(boundary)\r\n".data(using: .utf8)!)
            body.append("Content-Disposition: form-data; name=\"\(name)\"\r\n\r\n".data(using: .utf8)!)
            body.append("\(value)\r\n".data(using: .utf8)!)
        }
        
        // patientId field
        appendField(name: "patientId", value: patientId)
        
        // file field
        let filename = fileURL.lastPathComponent
        let fileData = try Data(contentsOf: fileURL)
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"file\"; filename=\"\(filename)\"\r\n".data(using: .utf8)!)
        // TODO: Detect actual mime type if needed. Using generic model
        body.append("Content-Type: model/vnd.usdz+zip\r\n\r\n".data(using: .utf8)!)
        body.append(fileData)
        body.append(lineBreak.data(using: .utf8)!)
        
        // closing boundary
        body.append("--\(boundary)--\r\n".data(using: .utf8)!)
        return body
    }
}
