#!/usr/bin/env swift
// Get OCR'd text from an image using Live Text in macOS.
//
// If you're using Preview, you can use Live Text to copy and paste text
// that's in an image.  This script allows you to access that text
// programatically, which is useful if you want to do bulk analysis of
// the text in your images.
//
// You can search text in the Photos app, but this is useful if you:
//
//    - want to search images that aren't in your Photos library
//    - want to do analysis which isn't just searching
//
// This is based on https://developer.apple.com/documentation/vision/recognizing_text_in_images
//
// Tested on macOS Monterey.
//
// You may need to run `chmod +x get_live_text` first and install the Xcode
// command-line tools.
//
// == Usage ==
//
// Pass the path to your image as a single command-line argument.  Any text
// in the image will be returned as a JSON list:
//
//      $ get_live_text railway-sign.jpg
//      ["Passengers must","not pass this point","or cross the line"]
//
// If the image doesn't contain any text, it returns an empty list:
//
//      $ get_live_text dancers.jpg
//      []
//

import Vision

// Process the results of the text-recognition request.
//
// This is based on the code in Apple's documentation, and prints the
// recognized text as a list of JSON strings.
//
// See https://developer.apple.com/documentation/vision/recognizing_text_in_images#3601255
func recognizeTextHandler(request: VNRequest, error: Error?) {
  guard
    let observations =
      request.results as? [VNRecognizedTextObservation]
  else {
    return
  }
  let recognizedStrings = observations.compactMap { observation in
    // Return the string of the top VNRecognizedText instance.
    return observation.topCandidates(1).first?.string
  }

  // Serialise to JSON
  do {
    let jsonData = try JSONSerialization.data(withJSONObject: recognizedStrings)

    if let JSONString = String(data: jsonData, encoding: String.Encoding.utf8) {
      print(JSONString)
    }
  } catch {
    fputs("Unable to serialise the result as JSON: \(error).\n", stderr)
    exit(1)
  }
}

// Given the path to an image, print a JSON array of text it contains.
func printTextInImage(imagePath: String) {
  let requestHandler = VNImageRequestHandler(
    url: URL(fileURLWithPath: imagePath),
    options: [:]
  )

  let request = VNRecognizeTextRequest(completionHandler: recognizeTextHandler)

  do {
    // Perform the text-recognition request.
    try requestHandler.perform([request])
  } catch {
    fputs("Unable to recognise text: \(error).\n", stderr)
    exit(1)
  }
}

let arguments = CommandLine.arguments

if arguments.count != 2 {
  fputs("Usage: \(arguments[0]) PATH\n", stderr)
  exit(1)
}

printTextInImage(imagePath: arguments[1])
