//
//  Downloader.swift
//  Data Manager
//
//  Created by Gabriel Jacoby-Cooper on 10/31/21.
//

import Foundation

#if canImport(FoundationNetworking)
import FoundationNetworking
#endif // canImport(FoundationNetworking)

final class Downloader {
	
	private static let remoteURL = URL(string: "https://shuttletracker.app/buses")!
	
	private let fileHandle: FileHandle
	
	private var recentBuses = Set<Bus>()
	
	init?(savingDataAtPath path: String) throws {
		guard FileManager.default.isWritableFile(atPath: path) else {
			return nil
		}
		let localURL = URL(fileURLWithPath: path)
		self.fileHandle = try FileHandle(forUpdating: localURL)
	}
	
	deinit {
		print("[\(Date())] Stopping...")
		try! self.fileHandle.close()
	}
	
	func saveSnapshot() async throws {
		let session = URLSession(configuration: .ephemeral)
		let (data, _) = try await session.data(from: Self.remoteURL)
		let decoder = JSONDecoder()
		decoder.dateDecodingStrategy = .iso8601
		let buses = try decoder.decode([Bus].self, from: data)
		for bus in buses {
			if !self.recentBuses.contains(bus) && bus.location.date.timeIntervalSinceNow > -30 {
				let line = "\(bus.id),\(bus.location.coordinate.latitude),\(bus.location.coordinate.longitude),\(bus.location.date),\(bus.location.type)\n"
				guard let lineData = line.data(using: .utf8) else {
					continue
				}
				print("[\(Date())] Saving snapshot of bus \(bus.id)...")
				try self.fileHandle.seekToEnd()
				try self.fileHandle.write(contentsOf: lineData)
			}
		}
		self.recentBuses = Set(buses)
	}
	
}
