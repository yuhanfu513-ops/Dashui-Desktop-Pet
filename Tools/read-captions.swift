import AppKit
import AVFoundation
import Vision
let url=URL(fileURLWithPath:CommandLine.arguments[1]);let tag=CommandLine.arguments[2];let seconds=Int(CommandLine.arguments[3])!
let asset=AVURLAsset(url:url);let gen=AVAssetImageGenerator(asset:asset);gen.appliesPreferredTrackTransform=true;gen.maximumSize=CGSize(width:1080,height:1920)
var rows:[[String:Any]]=[]
for i in 0..<(seconds*2) {
 do {
  let cg=try gen.copyCGImage(at:CMTime(seconds:Double(i)/2,preferredTimescale:600),actualTime:nil)
  if i%8==2 { let image=NSBitmapImageRep(cgImage:cg);try image.representation(using:.png,properties:[:])!.write(to:URL(fileURLWithPath:"Work/\(tag)-\(i).png")) }
  let req=VNRecognizeTextRequest();req.recognitionLevel = .accurate;req.recognitionLanguages=["zh-Hans","en-US"];req.usesLanguageCorrection=true
  try VNImageRequestHandler(cgImage:cg,options:[:]).perform([req])
  let lines=(req.results ?? []).compactMap { r -> [String:Any]? in guard let s=r.topCandidates(1).first else{return nil};return ["text":s.string,"x":r.boundingBox.minX,"y":r.boundingBox.minY] }
  rows.append(["time":Double(i)/2,"lines":lines])
 } catch { print("\(tag) frame \(i): \(error)") }
}
try JSONSerialization.data(withJSONObject:rows,options:[.prettyPrinted,.sortedKeys]).write(to:URL(fileURLWithPath:"Work/\(tag)-ocr.json"))
print("OCR \(tag) done")
