import subprocess
import tkinter as tk
from tkinter import ttk, messagebox


root = tk.Tk()
root.title("Public WiFi Security Analyzer")
root.geometry("1000x550")
root.configure(bg="#0f172a")


style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview",
                background="#1e293b",
                foreground="white",
                rowheight=28,
                fieldbackground="#1e293b",
                font=("Segoe UI", 10))

style.configure("Treeview.Heading",
                background="#0ea5e9",
                foreground="black",
                font=("Segoe UI", 11, "bold"))

style.map("Treeview",
          background=[("selected", "#2563eb")])


title = tk.Label(root,
                 text="🔐 Public WiFi Security Analyzer",
                 font=("Segoe UI", 20, "bold"),
                 bg="#0f172a",
                 fg="#38bdf8")
title.pack(pady=15)

subtitle = tk.Label(root,
                    text="SSID Comparison & Open Network Detection",
                    font=("Segoe UI", 12),
                    bg="#0f172a",
                    fg="white")
subtitle.pack()


columns = ("SSID", "BSSID", "Signal", "Security", "Risk Level")

tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=180)

tree.pack(fill="both", expand=True, padx=30, pady=20)


tree.tag_configure("safe", background="#14532d")
tree.tag_configure("danger", background="#7f1d1d")
tree.tag_configure("suspicious", background="#78350f")


status_label = tk.Label(root,
                        text="Click Scan to analyze networks...",
                        bg="#0f172a",
                        fg="#94a3b8",
                        font=("Segoe UI", 10))
status_label.pack(pady=5)


def scan_wifi():
    tree.delete(*tree.get_children())
    status_label.config(text="Scanning networks...")

    try:
       
        subprocess.call("netsh wlan scan", shell=True)

        output = subprocess.check_output(
            "netsh wlan show networks mode=bssid",
            shell=True
        ).decode(errors="ignore")

        networks = []
        current_ssid = None
        current_auth = None
        current_encryption = None
        current_bssid = None

        for line in output.split("\n"):
            line = line.strip()

            if line.startswith("SSID") and "BSSID" not in line:
                current_ssid = line.split(":", 1)[1].strip()

            elif line.startswith("Authentication"):
                current_auth = line.split(":", 1)[1].strip()

            elif line.startswith("Encryption"):
                current_encryption = line.split(":", 1)[1].strip()

            elif line.startswith("BSSID"):
                current_bssid = line.split(":", 1)[1].strip()

            elif line.startswith("Signal"):
                signal = line.split(":", 1)[1].strip()

                
                if not current_ssid:
                    continue

                networks.append({
                    "ssid": current_ssid,
                    "bssid": current_bssid,
                    "signal": signal,
                    "auth": current_auth,
                    "encryption": current_encryption
                })

       
        unique_networks = []
        seen_bssid = set()

        for net in networks:
            if net["bssid"] not in seen_bssid:
                unique_networks.append(net)
                seen_bssid.add(net["bssid"])

       
        ssid_count = {}
        for net in unique_networks:
            ssid_count[net["ssid"]] = ssid_count.get(net["ssid"], 0) + 1

        total_networks = 0

        for net in unique_networks:
            total_networks += 1

            risk = "Safe"
            tag = "safe"

           
            if net["encryption"] == "None" or net["auth"] == "Open":
                risk = "Dangerous (Open Network)"
                tag = "danger"

            
            elif ssid_count[net["ssid"]] > 1:
                risk = "Suspicious (Duplicate SSID)"
                tag = "suspicious"

            
            elif int(net["signal"].replace("%", "")) < 15:
                risk = "Weak Signal"
                tag = "suspicious"

            
            elif "WPA3" in net["auth"]:
                risk = "Safest WiFi"
                tag = "safe"

            tree.insert("", tk.END,
                        values=(net["ssid"],
                                net["bssid"],
                                net["signal"],
                                net["auth"],
                                risk),
                        tags=(tag,))

        status_label.config(text=f"Scan Complete: {total_networks} networks found")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        status_label.config(text="Error occurred during scan")


scan_btn = tk.Button(root,
                     text="Scan WiFi Networks",
                     command=scan_wifi,
                     bg="#0ea5e9",
                     fg="black",
                     font=("Segoe UI", 12, "bold"),
                     padx=20,
                     pady=8,
                     relief="flat")

scan_btn.pack(pady=10)

root.mainloop()
