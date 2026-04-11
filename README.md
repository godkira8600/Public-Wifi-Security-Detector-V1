# 🔐 Public WiFi Security Detector V1

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![GUI](https://img.shields.io/badge/GUI-Tkinter-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-1.0-red?style=for-the-badge)

> A lightweight Windows desktop tool that scans nearby Wi-Fi networks, detects open/unsecured hotspots, flags duplicate SSIDs (evil twin attack indicators), and color-codes every result by risk level — all in a clean dark-mode GUI.

---

## 📸 Preview

```
┌─────────────────────────────────────────────────────────────────┐
│          🔐 Public WiFi Security Analyzer                       │
│          SSID Comparison & Open Network Detection               │
├──────────────┬──────────────┬────────┬────────────┬────────────┤
│ SSID         │ BSSID        │ Signal │ Security   │ Risk Level │
├──────────────┼──────────────┼────────┼────────────┼────────────┤
│ CoffeeShop   │ AA:BB:CC:... │  87%   │ WPA3       │ Safest     │  🟢
│ FreeWiFi     │ 11:22:33:... │  72%   │ Open       │ Dangerous  │  🔴
│ Airport_Free │ DE:AD:BE:... │  65%   │ WPA2       │ Suspicious │  🟡
└──────────────┴──────────────┴────────┴────────────┴────────────┘
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Live Network Scan** | Triggers a fresh `netsh wlan scan` on every button click for up-to-date results |
| 🔓 **Open Network Detection** | Flags any network with `Authentication: Open` or `Encryption: None` as **Dangerous** |
| 👥 **Duplicate SSID Detection** | Identifies potential **evil twin / rogue AP attacks** by spotting multiple BSSIDs sharing the same SSID |
| 📶 **Weak Signal Warning** | Networks below 15% signal strength are flagged as **Suspicious** |
| 🛡️ **WPA3 Recognition** | Explicitly marks WPA3-secured networks as the **Safest** option |
| 🎨 **Color-Coded Risk UI** | Dark green = safe, amber = suspicious, red = dangerous — at a glance |
| 🖥️ **Zero-Dependency GUI** | Built entirely on Python's built-in `tkinter` — no external packages needed |

---

## 🚀 Getting Started

### Prerequisites

- **OS:** Windows 10 or Windows 11
- **Python:** 3.7 or higher
- **Wi-Fi adapter** present and enabled

> ⚠️ This tool uses `netsh` (Windows Network Shell). It will **not** work on macOS or Linux.

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/godkira8600/Public-Wifi-Security-Detector-V1.git

# 2. Navigate into the project directory
cd Public-Wifi-Security-Detector-V1
```

No `pip install` required — all dependencies are part of Python's standard library.

### Run

```bash
python public_wifi_protector.py
```

> 💡 **Tip:** Run from a terminal with standard user privileges. Administrator rights are not required for scanning.

---

## 🧠 How It Works

The tool orchestrates two Windows `netsh` commands under the hood:

```
netsh wlan scan                          # Forces a fresh radio scan
netsh wlan show networks mode=bssid      # Dumps full network details
```

The raw output is then parsed line-by-line to extract each network's **SSID**, **BSSID**, **Signal %**, **Authentication**, and **Encryption** type. Each network is evaluated against this risk matrix:

```
┌──────────────────────────────────────────────────────┬──────────────────────────────┬───────┐
│ Condition                                            │ Risk Label                   │ Color │
├──────────────────────────────────────────────────────┼──────────────────────────────┼───────┤
│ Encryption == None OR Authentication == Open         │ ⛔ Dangerous (Open Network)  │ Red   │
│ Multiple BSSIDs share the same SSID                  │ ⚠️  Suspicious (Dup. SSID)   │ Amber │
│ Signal strength < 15%                                │ ⚠️  Weak Signal              │ Amber │
│ Authentication contains "WPA3"                       │ ✅ Safest WiFi               │ Green │
│ None of the above                                    │ ✅ Safe                      │ Green │
└──────────────────────────────────────────────────────┴──────────────────────────────┴───────┘
```

---

## 📁 Project Structure

```
Public-Wifi-Security-Detector-V1/
│
└── public_wifi_protector.py    # Single-file application (UI + scan logic)
```

---

## 🛠️ Built With

| Technology | Purpose |
|---|---|
| `tkinter` + `ttk` | GUI window, table (Treeview), labels, and buttons |
| `subprocess` | Executes `netsh` commands and captures output |
| `Python 3` | Core language — no virtual environment needed |

---

## ⚠️ Limitations & Known Issues

- **Windows only** — relies exclusively on `netsh wlan` which is not available on macOS/Linux.
- **No real-time monitoring** — the scan is a one-shot operation triggered by the button; there is no background polling.
- **Signal parsing** — assumes signal values are formatted as `XX%`; unusual adapter outputs may cause parsing edge cases.
- **Admin rights** — in some corporate or restricted environments, `netsh wlan scan` may require elevated privileges.
- **Hidden SSIDs** — networks broadcasting an empty SSID are skipped during parsing.

---

## 🔮 Roadmap / Potential Improvements

- [ ] Auto-refresh / continuous monitoring mode
- [ ] Export scan results to CSV or JSON
- [ ] macOS support via `airport` CLI utility
- [ ] Linux support via `nmcli` / `iwlist`
- [ ] Vendor lookup from BSSID (OUI database)
- [ ] Notification/alert sound on dangerous network detection
- [ ] Historical scan comparison to detect new rogue APs

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** this repository
2. **Create** a feature branch: `git checkout -b feature/your-feature-name`
3. **Commit** your changes: `git commit -m "Add: your feature description"`
4. **Push** to the branch: `git push origin feature/your-feature-name`
5. **Open** a Pull Request

Please keep pull requests focused and include a clear description of what changed and why.

---

## 📄 License

This project is open source. Feel free to use, modify, and distribute it in accordance with the [MIT License](LICENSE).

---

## 👤 Authors

**godkira8600** , **vaishnavpt06**

- GitHub: [@godkira8600](https://github.com/godkira8600) , [@vaishnavpt06](https://github.com/vaishnavpt06)

---

> **Disclaimer:** This tool is intended for **educational and personal security awareness** purposes only. Always obtain proper authorization before scanning networks that you do not own or administer. The author is not responsible for any misuse of this software.
