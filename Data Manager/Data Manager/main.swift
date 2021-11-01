//
//  main.swift
//  Data Manager
//
//  Created by Gabriel Jacoby-Cooper on 10/31/21.
//

import Foundation

func shutDown() {
	downloader = nil
	exit(EXIT_SUCCESS)
}

signal(SIGINT, SIG_IGN)
signal(SIGQUIT, SIG_IGN)
signal(SIGTERM, SIG_IGN)
let sigintSource = DispatchSource.makeSignalSource(signal: SIGINT)
let sigquitSource = DispatchSource.makeSignalSource(signal: SIGQUIT)
let sigtermSource = DispatchSource.makeSignalSource(signal: SIGTERM)
sigintSource.setEventHandler(handler: shutDown)
sigquitSource.setEventHandler(handler: shutDown)
sigtermSource.setEventHandler(handler: shutDown)
sigintSource.resume()
sigquitSource.resume()
sigtermSource.resume()
if CommandLine.arguments.count != 2 || CommandLine.arguments[1] == "-h" || CommandLine.arguments[1] == "--help" {
	print("Usage: datamanager [options] data_file_path")
	print("  Options:")
	print("    -h, --help\tShows this message")
	exit(EXIT_SUCCESS)
}
let path = CommandLine.arguments[1].expandingTildeInPath
if !FileManager.default.fileExists(atPath: path) {
	guard FileManager.default.createFile(atPath: path, contents: nil) else {
		errorPrint("Couldn't create data file; do you have the appropriate permissions?")
		exit(EXIT_FAILURE)
	}
}
var downloader = try Downloader(savingDataAtPath: path)
guard downloader != nil else {
	errorPrint("Couldn't initialize downloader; is the specified path writable?")
	exit(EXIT_FAILURE)
}
Timer.scheduledTimer(withTimeInterval: 5, repeats: true) { (_) in
	do {
		try downloader!.saveSnapshot()
	} catch {
		errorPrint("Failed to save snapshot")
	}
}
RunLoop.current.run()
