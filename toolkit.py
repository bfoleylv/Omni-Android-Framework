import os
import subprocess
import sys
import logging
import tkinter as tk
from tkinter import ttk, messagebox

logging.basicConfig(
    filename='/home/bfoleylv/androidtoolkit_build/toolkit_errors.log',
    level=logging.ERROR,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

class OmniFramework:
    def __init__(self, root):
        self.root = root
        self.root.title("Omni-Android-Framework v1.5")
        self.root.geometry("1100x750")
        self.root.configure(bg="#121212")

        self.base_dir = "/home/bfoleylv/androidtoolkit_build"
        self.driver_dir = os.path.join(self.base_dir, "drivers")
        self.plugin_dir = os.path.join(self.base_dir, "plugins")
        self.sensor_dir = os.path.join(self.base_dir, "sensors")

        self.setup_ui()
        self.refresh_diagnostics()
        self.build_plugin_tabs()

    def setup_ui(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TNotebook", background="#1e1e1e", borderwidth=0)
        self.style.configure("TNotebook.Tab", background="#333333", foreground="#00ff00")
        self.style.map("TNotebook.Tab", background=[("selected", "#00ff00")], foreground=[("selected", "#000000")])

        self.paned = ttk.PanedWindow(self.root, orient="horizontal")
        self.paned.pack(expand=True, fill="both")

        self.left_frame = tk.Frame(self.paned, bg="#000000", width=350)
        self.paned.add(self.left_frame)
        
        tk.Label(self.left_frame, text="DEVICE STATUS", bg="#000000", fg="#00ff00", font=("Courier", 12, "bold")).pack(pady=5)
        self.console = tk.Text(self.left_frame, bg="#000000", fg="#00ff00", font=("Courier", 10), borderwidth=0)
        self.console.pack(expand=True, fill="both", padx=10)

        # Only the Hard Reset for Drivers stays here for stability
        btn_frame = tk.Frame(self.left_frame, bg="#000000")
        btn_frame.pack(fill="x", side="bottom", pady=10)
        tk.Button(btn_frame, text="FIX DRIVERS", bg="#cc0000", fg="white", font=("Courier", 10, "bold"), command=self.fix_drivers).pack(fill="x", padx=10)

        self.right_frame = tk.Frame(self.paned, bg="#1e1e1e")
        self.paned.add(self.right_frame)
        self.notebook = ttk.Notebook(self.right_frame)
        self.notebook.pack(expand=True, fill="both", padx=5, pady=5)

    def fix_drivers(self):
        try:
            cmd = "echo 'SUBSYSTEM==\"usb\", ATTR{idVendor}==\"*\", MODE=\"0666\", GROUP=\"plugdev\"' | sudo tee /etc/udev/rules.d/51-android.rules && sudo udevadm control --reload-rules && sudo udevadm trigger"
            subprocess.run(cmd, shell=True)
            subprocess.run(["sudo", "modprobe", "usbserial", "vendor=0x05c6", "product=0x9008"])
            self.console.insert(tk.END, "\n[+] DRIVERS RELOADED")
        except Exception as e:
            logging.error(f"Driver fix failed: {e}")

    def refresh_diagnostics(self):
        self.console.delete("1.0", tk.END)
        self.console.insert(tk.END, "--- SCANNING HARDWARE ---\n")
        try:
            model = subprocess.check_output(["adb", "shell", "getprop", "ro.product.model"], text=True, timeout=2).strip() or "OnePlus 8"
            ver = subprocess.check_output(["adb", "shell", "getprop", "ro.build.version.release"], text=True, timeout=2).strip()
            batt = subprocess.check_output("adb shell dumpsys battery | grep level", shell=True, text=True, timeout=2).split(":")[1].strip()
            self.console.insert(tk.END, f"\nDEVICE: {model}\nOS: Android {ver}\nBATTERY: {batt}%")
        except:
            try:
                fb = subprocess.check_output(["fastboot", "devices"], text=True, timeout=2).strip()
                if fb: self.console.insert(tk.END, f"\n[!] MODE: FASTBOOT ACTIVE\nID: {fb.split()[0]}")
                else: self.console.insert(tk.END, "\n[?] STATUS: DISCONNECTED")
            except:
                self.console.insert(tk.END, "\n[?] STATUS: DISCONNECTED")
        self.root.after(10000, self.refresh_diagnostics)

    def build_plugin_tabs(self):
        if not os.path.exists(self.plugin_dir): return
        # Clear existing tabs
        for tab in self.notebook.tabs():
            self.notebook.forget(tab)
        for folder in sorted(os.listdir(self.plugin_dir)):
            full_path = os.path.join(self.plugin_dir, folder)
            if os.path.isdir(full_path):
                tab = tk.Frame(self.notebook, bg="#1e1e1e")
                self.notebook.add(tab, text=folder.lower())
                for file in sorted(os.listdir(full_path)):
                    if file.endswith(".py"):
                        btn = ttk.Button(tab, text=file[:-3].replace("_", " ").upper(), 
                                       command=lambda f=folder, n=file: self.run_tool(f, n))
                        btn.pack(pady=5, padx=20, fill="x")

    def run_tool(self, category, filename):
        target = os.path.join(self.plugin_dir, category, filename)
        env = os.environ.copy()
        env["OMNI_DRIVER_PAYLOAD"] = self.driver_dir
        try:
            subprocess.Popen([sys.executable, target], env=env)
        except Exception as e:
            logging.error(f"Plugin failed: {filename} - {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = OmniFramework(root)
    root.mainloop()
