import Foundation

final class APIClient {
    static let shared = APIClient()
    
    private init() {}
    
    private let baseURL = URL(string: "https://api.rhinovate.ai")! // change to your real one
    
    func uploadScan(fileURL: URL) async throws -> AnalysisResult {
        let endpoint = baseURL.appendingPathComponent("/analyze-scan")
        
        var request = URLRequest(url: endpoint)
        request.httpMethod = "POST"
        
        // multipart
        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        
        let data = try createMultipartBody(fileURL: fileURL, boundary: boundary, fieldName: "file", fileName: fileURL.lastPathComponent)
        
        let (responseData, response) = try await URLSession.shared.upload(for: request, from: data)
        
        guard let httpResponse = response as? HTTPURLResponse,
              200..<300 ~= httpResponse.statusCode else {
            throw URLError(.badServerResponse)
        }
        
        let decoder = JSONDecoder()
        return try decoder.decode(AnalysisResult.self, from: responseData)
    }
    
    private func createMultipartBody(fileURL: URL, boundary: String, fieldName: String, fileName: String) throws -> Data {
        var body = Data()
        let lineBreak = "\r\n"
        
        body.appendString("--\(boundary)\r\n")
        body.appendString("Content-Disposition: form-data; name=\"\(fieldName)\"; filename=\"\(fileName)\"\r\n")
        body.appendString("Content-Type: application/octet-stream\r\n\r\n")
        let fileData = try Data(contentsOf: fileURL)
        body.append(fileData)
        body.appendString("\r\n")
        body.appendString("--\(boundary)--\r\n")
        
        return body
    }
}

fileprivate extension Data {
    mutating func appendString(_ string: String) {
        self.append(Data(string.utf8))
    }
}

