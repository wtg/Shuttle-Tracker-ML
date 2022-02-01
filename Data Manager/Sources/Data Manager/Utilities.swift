//
//  Utilities.swift
//  Data Manager
//
//  Created by Gabriel Jacoby-Cooper on 10/31/21.
//

import Foundation

#if canImport(FoundationNetworking)
import FoundationNetworking
#endif // canImport(FoundationNetworking)

func errorPrint(_ items: Any...) {
	#if os(macOS) || os(Linux)
		for item in items.dropLast() {
			print(item, terminator: " ", to: &stderr)
		}
		if let lastItem = items.last {
			print(lastItem, to: &stderr)
		}
	#else // os(macOS) || os(Linux)
		for item in items.dropLast() {
			print(item, terminator: " ")
		}
		if let lastItem = items.last {
			print(lastItem)
		}
	#endif // os(macOS) || os(Linux)
}

extension String {
	
	var expandingTildeInPath: String {
		get {
			return NSString(string: self).expandingTildeInPath
		}
	}
	
}

extension UnsafeMutablePointer: TextOutputStream where Pointee == FILE {
	
	public func write(_ string: String) {
		fputs(string, self)
	}
	
}

#if os(Linux)
extension Date {
	
	static var now: Date {
		get {
			return Date()
		}
	}
	
}

extension URLSession {
	
	func data(from url: URL) async throws -> (Data, URLResponse) {
		try await withCheckedThrowingContinuation { (continuation) in
			let task = self.dataTask(with: url) { (data, response, error) in
				guard let data = data, let response = response else {
					let error = error ?? URLError(.badServerResponse)
					return continuation.resume(throwing: error)
				}
				continuation.resume(returning: (data, response))
			}
			task.resume()
		}
	}
	
}
#endif // os(Linux)
