//
//  Bus.swift
//  Data Manager
//
//  Created by Gabriel Jacoby-Cooper on 11/1/21.
//

import Foundation

struct Bus: Decodable, Hashable, Equatable {
	
	struct Location: Decodable, Hashable, Equatable {
		
		enum LocationType: String, Decodable {
			
			case system = "system"
			
			case user = "user"
			
		}
		
		struct Coordinate: Decodable, Hashable, Equatable {
			
			let latitude: Double
			
			let longitude: Double
			
		}
		
		let id: UUID
		
		let date: Date
		
		let coordinate: Coordinate
		
		let type: LocationType
		
		static func == (_ left: Location, _ right: Location) -> Bool {
			return left.date == right.date && left.coordinate == right.coordinate && left.type == right.type
		}
		
		func hash(into hasher: inout Hasher) {
			hasher.combine(self.date)
			hasher.combine(self.coordinate)
			hasher.combine(self.type)
		}
		
	}
	
	let id: Int
	
	let location: Location
	
	static func == (_ left: Bus, _ right: Bus) -> Bool {
		return left.id == right.id && left.location == right.location
	}
	
	func hash(into hasher: inout Hasher) {
		hasher.combine(self.id)
		hasher.combine(self.location)
	}
	
}
