// Usage: swift render.swift <pdf> <outdir> <scale>
// Renders each PDF page to PNG and prints each page's text.
import Foundation
import PDFKit
import AppKit

let args = CommandLine.arguments
let pdfURL = URL(fileURLWithPath: args[1])
let outDir = URL(fileURLWithPath: args[2])
let scale = CGFloat(Double(args[3]) ?? 2.0)
try? FileManager.default.createDirectory(at: outDir, withIntermediateDirectories: true)

guard let doc = PDFDocument(url: pdfURL) else { print("cannot open"); exit(1) }
print("pages: \(doc.pageCount)")
for i in 0..<doc.pageCount {
    guard let page = doc.page(at: i) else { continue }
    let box = page.bounds(for: .mediaBox)
    let w = Int(box.width * scale), h = Int(box.height * scale)
    let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: w, pixelsHigh: h,
                               bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false,
                               colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
    NSGraphicsContext.saveGraphicsState()
    let ctx = NSGraphicsContext(bitmapImageRep: rep)!
    NSGraphicsContext.current = ctx
    let cg = ctx.cgContext
    cg.setFillColor(NSColor.white.cgColor)
    cg.fill(CGRect(x: 0, y: 0, width: w, height: h))
    cg.scaleBy(x: scale, y: scale)
    page.draw(with: .mediaBox, to: cg)
    NSGraphicsContext.restoreGraphicsState()
    let png = rep.representation(using: .png, properties: [:])!
    let name = String(format: "page-%02d.png", i + 1)
    try png.write(to: outDir.appendingPathComponent(name))
    let text = (page.string ?? "").replacingOccurrences(of: "\n", with: " | ")
    print("\(name) \(w)x\(h): \(text.prefix(300))")
}
