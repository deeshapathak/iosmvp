//
//  Item.swift
//  Rhinovate
//
//  Created by Deesha Pathak on 11/14/25.
//

import Foundation
import SwiftData

@Model
final class Item {
    var timestamp: Date
    
    init(timestamp: Date) {
        self.timestamp = timestamp
    }
}
