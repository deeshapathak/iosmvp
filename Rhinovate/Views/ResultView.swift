import SwiftUI

struct ResultView: View {
    let result: AnalysisResult
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                Text("Your AI Plan")
                    .font(.title2.bold())
                
                if let summary = result.analysis_summary {
                    Text(summary)
                        .foregroundColor(.secondary)
                        .padding(.bottom, 8)
                }
                
                if let areas = result.areas, !areas.isEmpty {
                    ForEach(areas) { area in
                        VStack(alignment: .leading, spacing: 4) {
                            Text(area.area ?? "Area")
                                .font(.headline)
                            if let issue = area.issue {
                                Text(issue)
                                    .font(.subheadline)
                                    .foregroundColor(.secondary)
                            }
                            if let suggestion = area.suggestion {
                                Text("Suggestion: \(suggestion)")
                                    .font(.subheadline)
                                    .foregroundColor(.blue)
                            }
                        }
                        .padding()
                        .background(Color(.secondarySystemBackground))
                        .cornerRadius(10)
                    }
                } else {
                    Text("No issues detected 🎉")
                        .foregroundColor(.secondary)
                }
            }
            .padding()
        }
        .navigationTitle("Results")
        .navigationBarTitleDisplayMode(.inline)
    }
}

