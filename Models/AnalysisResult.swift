import Foundation

struct AnalysisResult: Codable, Hashable, Identifiable {
    var id: UUID = UUID()
    let analysis_summary: String?
    let areas: [AnalysisArea]?
}

struct AnalysisArea: Codable, Identifiable, Hashable {
    var id: UUID = UUID()
    let area: String?
    let issue: String?
    let suggestion: String?
    let show_simulation: Bool?
}

