//
//  Downloader.swift
//  Data Manager
//
//  Created by Gabriel Jacoby-Cooper on 10/31/21.
//

import Foundation

final class Downloader {
	
	private static let remoteURL = URL(string: "https://shuttletracker.app/buses")!
	
	private let fileHandle: FileHandle
	
	func saveSnapshot() throws {
		print("[\(Date.now)] Saving snapshot...")
		var rawString = try String(contentsOf: Self.remoteURL)
		rawString.removeAll { (character) in
			return character.isWhitespace
		}
		guard rawString != "[]" else {
			return
		}
		rawString.append(contentsOf: "\n")
		guard let data = rawString.data(using: .utf8) else {
			return
		}
		try self.fileHandle.seekToEnd()
		try self.fileHandle.write(contentsOf: data)
	}
	
	init?(savingDataAtPath path: String) throws {
		guard FileManager.default.isWritableFile(atPath: path) else {
			return nil
		}
		let localURL = URL(fileURLWithPath: path)
		self.fileHandle = try FileHandle(forUpdating: localURL)
	}
	
	deinit {
		print("Stopping...")
		try! self.fileHandle.close()
	}
	
}
