import Cocoa
import WebKit

class WindowDelegate: NSObject, NSWindowDelegate {
    func windowWillClose(_ notification: Notification) {
        NSApplication.shared.terminate(nil)
    }
}

class AppDelegate: NSObject, NSApplicationDelegate {
    var window: NSWindow!
    let windowDelegate = WindowDelegate()

    func applicationDidFinishLaunching(_ notification: Notification) {
        let screenRect = NSScreen.main?.visibleFrame ?? NSRect(x: 0, y: 0, width: 1440, height: 900)
        let width = min(1480, screenRect.width * 0.92)
        let height = min(940, screenRect.height * 0.92)
        let rect = NSRect(
            x: screenRect.origin.x + (screenRect.width - width) / 2,
            y: screenRect.origin.y + (screenRect.height - height) / 2,
            width: width,
            height: height
        )

        window = NSWindow(
            contentRect: rect,
            styleMask: [.titled, .closable, .miniaturizable, .resizable],
            backing: .buffered,
            defer: false
        )
        window.title = "Agent Hub 2.0"
        window.titleVisibility = .visible
        window.titlebarAppearsTransparent = false
        window.backgroundColor = NSColor(red: 0.02, green: 0.03, blue: 0.05, alpha: 1.0)
        window.delegate = windowDelegate
        
        let config = WKWebViewConfiguration()
        let webView = WKWebView(frame: window.contentView!.bounds, configuration: config)
        webView.autoresizingMask = [.width, .height]
        webView.setValue(false, forKey: "drawsBackground") // dark transparent feel
        window.contentView?.addSubview(webView)

        if let iconPath = Bundle.main.path(forResource: "AppIcon", ofType: "icns"),
           let iconImg = NSImage(contentsOfFile: iconPath) {
            NSApplication.shared.applicationIconImage = iconImg
        }

        if let url = URL(string: "http://127.0.0.1:8765") {
            webView.load(URLRequest(url: url))
        }

        window.makeKeyAndOrderFront(nil)
        NSApplication.shared.activate(ignoringOtherApps: true)
    }
}

let app = NSApplication.shared
let delegate = AppDelegate()
app.delegate = delegate
app.setActivationPolicy(.regular)
app.run()
