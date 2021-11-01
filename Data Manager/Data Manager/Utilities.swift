//
//  Utilities.swift
//  Data Manager
//
//  Created by Gabriel Jacoby-Cooper on 10/31/21.
//

import Foundation

func errorPrint(_ items: Any...) {
	for item in items.dropLast() {
		print(item, terminator: " ", to: &stderr)
	}
	if let lastItem = items.last {
		print(lastItem, to: &stderr)
	}
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
