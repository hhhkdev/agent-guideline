import Cocoa
import Foundation

class AgentHubStatusBarApp: NSObject, NSApplicationDelegate {
    var statusItem: NSStatusItem!
    var timer: Timer?

    func applicationDidFinishLaunching(_ aNotification: Notification) {
        // Create Status Bar Item
        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)
        
        if let button = statusItem.button {
            button.title = "⚡ AH: 로딩..."
        }

        setupMenu()
        updateTokenMetrics()

        // Schedule periodic update every 10 seconds
        timer = Timer.scheduledTimer(withTimeInterval: 10.0, repeats: true) { [weak self] _ in
            self?.updateTokenMetrics()
        }
    }

    func setupMenu() {
        let menu = NSMenu()
        
        let headerItem = NSMenuItem(title: "🛡️ Agent Hub 2.0 상태바 모니터", action: nil, keyEquivalent: "")
        headerItem.isEnabled = false
        menu.addItem(headerItem)
        menu.addItem(NSMenuItem.separator())

        let openItem = NSMenuItem(title: "🖥️ Agent Hub 대시보드 열기", action: #selector(openHub), keyEquivalent: "o")
        openItem.target = self
        menu.addItem(openItem)

        let portsItem = NSMenuItem(title: "🔌 실행 중인 포트 확인", action: #selector(openPorts), keyEquivalent: "p")
        portsItem.target = self
        menu.addItem(portsItem)

        let refreshItem = NSMenuItem(title: "🔄 쿼터 사용량 즉시 갱신", action: #selector(refreshNow), keyEquivalent: "r")
        refreshItem.target = self
        menu.addItem(refreshItem)

        menu.addItem(NSMenuItem.separator())
        let quitItem = NSMenuItem(title: "종료 (Quit)", action: #selector(quitApp), keyEquivalent: "q")
        quitItem.target = self
        menu.addItem(quitItem)

        statusItem.menu = menu
    }

    @objc func updateTokenMetrics() {
        guard let url = URL(string: "http://127.0.0.1:8765/api/tokens") else { return }
        let task = URLSession.shared.dataTask(with: url) { [weak self] data, response, error in
            guard let data = data, error == nil else {
                DispatchQueue.main.async {
                    self?.statusItem.button?.title = "⚡ AH: 오프라인"
                }
                return
            }

            do {
                if let json = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any],
                   let claude = json["claude"] as? [String: Any],
                   let claude5h = claude["last_5h"] as? [String: Any],
                   let claudePct = claude5h["pct_pro"] as? Double,
                   let gemini = json["gemini"] as? [String: Any],
                   let gemini5h = gemini["last_5h"] as? [String: Any],
                   let geminiPct = gemini5h["pct_pro"] as? Double,
                   let gpt = json["gpt"] as? [String: Any],
                   let gpt5h = gpt["last_5h"] as? [String: Any],
                   let gptPct = gpt5h["pct_pro"] as? Double {
                    
                    let titleStr = String(format: "⚡ C:%.0f%% G:%.0f%% O:%.0f%%", claudePct, geminiPct, gptPct)
                    DispatchQueue.main.async {
                        self?.statusItem.button?.title = titleStr
                    }
                }
            } catch {
                print("JSON parsing error: \(error)")
            }
        }
        task.resume()
    }

    @objc func openHub() {
        if let url = URL(string: "http://127.0.0.1:8765") {
            NSWorkspace.shared.open(url)
        }
    }

    @objc func openPorts() {
        if let url = URL(string: "http://127.0.0.1:8765#ports") {
            NSWorkspace.shared.open(url)
        }
    }

    @objc func refreshNow() {
        updateTokenMetrics()
    }

    @objc func quitApp() {
        NSApplication.shared.terminate(nil)
    }
}

let app = NSApplication.shared
let delegate = AgentHubStatusBarApp()
app.delegate = delegate
app.setActivationPolicy(.accessory) // Status bar only, no Dock icon
app.run()
