//
//  main.swift
//  Data Manager
//
//  Created by Gabriel Jacoby-Cooper on 10/31/21.
//

import Foundation
import ArgumentParser

@main final class DataManager: ParsableCommand {
	
	private enum CodingKeys: CodingKey {
		
		case outputPath, interval
		
	}
	
	private var downloader: Downloader?
	
	@Option(name: .shortAndLong, help: "The path to the data file.") private var outputPath: String
	
	@Option(name: .shortAndLong, help: "The interval (in seconds) between polls of the remote API.") private var interval: TimeInterval
	
	func run() throws {
		if ProcessInfo.processInfo.environment["SWIFT_WINDOWS"] != "TRUE" {
			signal(SIGINT, SIG_IGN)
			signal(SIGQUIT, SIG_IGN)
			signal(SIGTERM, SIG_IGN)
			let sigintSource = DispatchSource.makeSignalSource(signal: SIGINT)
			let sigquitSource = DispatchSource.makeSignalSource(signal: SIGQUIT)
			let sigtermSource = DispatchSource.makeSignalSource(signal: SIGTERM)
			sigintSource.setEventHandler(handler: self.shutDown)
			sigquitSource.setEventHandler(handler: self.shutDown)
			sigtermSource.setEventHandler(handler: self.shutDown)
			sigintSource.resume()
			sigquitSource.resume()
			sigtermSource.resume()
		}
		let extendedPath = self.outputPath.expandingTildeInPath
		if !FileManager.default.fileExists(atPath: extendedPath) {
			guard FileManager.default.createFile(atPath: extendedPath, contents: nil) else {
				errorPrint("Couldn't create data file; do you have the appropriate permissions?")
				throw Errors.dataFileCreationFailed
			}
		}
		self.downloader = try Downloader(savingDataAtPath: extendedPath)
		guard downloader != nil else {
			errorPrint("Couldn't initialize downloader; is the specified path writable?")
			throw Errors.downloaderInitializationFailed
		}
		print("[\(Date.now)] Starting...")
		_ = Timer.scheduledTimer(withTimeInterval: self.interval, repeats: true) { (_) in
			Task {
				try await self.downloader!.saveSnapshot()
			}
		}
		RunLoop.current.run()
	}
	
	private func shutDown() {
		self.downloader = nil
		Self.exit(withError: nil)
	}
	
}
