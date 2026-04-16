import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import subprocess
import os
import threading

class OmniFramework:
    def __init__(self, root):
        self.root = root
        self.root.title("Brandon's Omni-Framework v6.0 (Dynamic Tabs)")
        self.root.geometry("1200x900")
        self.root.configure(bg="#121212")

        # --- PATHS ---
        self.base_dir = os.path.expanduser("~/AndroidToolkit_Build")
        self.plugin_dir = f"{self.base_dir}/plugins"
        self.sensor_dir = f"{self.base_dir}/sensors"
        os.makedirs(self.plugin_dir, exist_ok=True)
        os.makedirs(self.sensor_dir, exist_ok=True)

        # --- UI LAYOUT ---
        self.left_panel = tk.Frame(root, bg="#1a1a1a", width=320)
        self.left_panel.pack(side="left", fill="y", padx=5, pady=5)
        
        tk.Label(self.left_panel, text="DEVICE DIAGNOSTICS", fg="#00ffcc", bg="#1a1a1a", font=("Arial", 12, "bold")).pack(pady=10)
        self.info_box = tk.Text(self.left_panel, bg="#000", fg="#0f0", font=("Courier", 10), height=35, width=38)
        self.info_box.pack(pady=5, padx=10)
        
        tk.Button(self.left_panel, text="FORCE RE-SCAN", command=self.update_info, bg="#00d1ff", fg="black", font=("Arial", 10, "bold")).pack(pady=10, fill="x", padx=20)
        tk.Button(self.left_panel, text="REFRESH TABS", command=self.build_tabs, bg="#9b59b6", fg="white").pack(pady=5, fill="x", padx=20)

        # --- THE DYNAMIC NOTEBOOK ---
        self.tabs = ttk.Notebook(root)
        self.tabs.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        self.build_tabs()
        self.update_loop()

    def build_tabs(self):
        # Clear existing tabs
        for tab in self.tabs.tabs():
            self.tabs.forget(tab)

        # Scan the plugins directory for sub-folders
        if not os.path.exists(self.plugin_dir): return

        folders = [d for d in os.listdir(self.plugin_dir) if os.path.isdir(os.path.join(self.plugin_dir, d))]
        
        # Sort them so Core/Safety usually comes first if they exist
        folders.sort()

        for folder_name in folders:
            # Create the Tab Frame
            tab_frame = tk.Frame(self.tabs, bg="#1c1c1c")
            nice_name = folder_name.replace("_", " ").title()
            self.tabs.add(tab_frame, text=f"  {nice_name}  ")

            # Create a Section for the Plugins in this folder
            full_path = os.path.join(self.plugin_dir, folder_name)
            self.populate_tab(tab_frame, nice_name, full_path)

    def populate_tab(self, parent, title, folder_path):
        frame = tk.LabelFrame(parent, text=title.upper(), fg="#00ffcc", bg="#1c1c1c", font=("Arial", 10, "bold"), padx=10, pady=10)
        frame.pack(fill="x", pady=10, padx=10)
        
        files = [f for f in os.listdir(folder_path) if f.endswith(".py")]
        if not files:
            tk.Label(frame, text="No scripts found in this category.", fg="#555", bg="#1c1c1c").pack()
            return

        for f in files:
            btn_name = f.replace(".py", "").replace("_", " ").title()
            script_path = os.path.join(folder_path, f)
            btn = tk.Button(frame, text=btn_name, command=lambda p=script_path: self.run_script(p), 
                           bg="#333", fg="white", width=22, pady=8, relief="flat")
            btn.pack(side="left", padx=5)

    def run_script(self, path):
        threading.Thread(target=lambda: subprocess.run(f"python3 '{path}'", shell=True), daemon=True).start()

    def update_info(self):
        self.info_box.config(state='normal')
        self.info_box.delete("1.0", tk.END)
        try:
            model = subprocess.run(['adb', 'shell', 'getprop', 'ro.product.model'], capture_output=True, text=True).stdout.strip()
            display_text = f"📱 MODEL: {model}\n---------------------------\n"

            # Dynamic Sensors
            if os.path.exists(self.sensor_dir):
                for f in os.listdir(self.sensor_dir):
                    if f.endswith(".py"):
                        res = subprocess.run(['python3', os.path.join(self.sensor_dir, f)], capture_output=True, text=True)
                        display_text += f"{res.stdout.strip()}\n"

            display_text += "---------------------------\nSTATUS: ONLINE"
            self.info_box.insert(tk.END, display_text)
        except:
            self.info_box.insert(tk.END, "DEVICE DISCONNECTED")
        self.info_box.config(state='disabled')

    def update_loop(self):
        self.update_info()
        self.root.after(5000, self.update_loop)

if __name__ == "__main__":
    root = tk.Tk()
    app = OmniFramework(root)
    root.mainloop()
