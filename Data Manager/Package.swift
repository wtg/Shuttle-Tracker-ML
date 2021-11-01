// swift-tools-version:5.5

import PackageDescription

let package = Package(
	name: "Data Manager",
	platforms: [
		.macOS(.v12)
	],
	dependencies: [
		.package(
			url: "https://github.com/apple/swift-argument-parser",
			.upToNextMajor(from: "1.0.0")
		)
	],
	targets: [
		.executableTarget(
			name: "Data Manager",
			dependencies: [
				.product(
					name: "ArgumentParser",
					package: "swift-argument-parser"
				)
			]
		)
	]
)
