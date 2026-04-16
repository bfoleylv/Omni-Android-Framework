import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3
import os

DB_PATH = "/home/bfoleylv/androidtoolkit_build/device_logs.db"
output_win = None
output_text = None

def init_db():
    conn = sqlite3.connect(DB_PATH)
    curr = conn.cursor()
    curr.execute('''CREATE TABLE IF NOT EXISTS hardware_vars 
                 (id INTEGER PRIMARY KEY, serial TEXT, variable TEXT, value TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def update_output(title, content):
    """Manages a single output window instance"""
    global output_win, output_text
    
    # If window exists, bring to front and refresh
    if output_win is not None and tk.Toplevel.winfo_exists(output_win):
        output_win.title(title)
        output_win.deiconify() # Un-minimize if hidden
        output_win.lift()      # Bring to front
        output_win.attributes("-topmost", True) # Flash to front
        output_win.attributes("-topmost", False)
        
        output_text.config(state="normal")
        output_text.delete("1.0", tk.END)
        output_text.insert("1.0", content)
        output_text.config(state="disabled")
    else:
        # Create new window
        output_win = tk.Toplevel()
        output_win.title(title)
        output_win.geometry("600x450")
        output_win.configure(bg="black")
        
        frame = tk.Frame(output_win, bg="black")
        frame.pack(expand=True, fill="both")
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        
        output_text = tk.Text(frame, bg="black", fg="#00ff00", font=("Courier", 10), yscrollcommand=scrollbar.set)
        output_text.pack(side="left", expand=True, fill="both")
        
        scrollbar.config(command=output_text.yview)
        output_text.insert("1.0", content)
        output_text.config(state="disabled")

def run_cmd(cmd, entry_widget=None):
    if entry_widget: cmd = entry_widget.get()
    if not cmd: return
    try:
        result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=300)
        formatted = f"EXECUTING: {cmd}\n\nSTDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
        update_output("Command Console", formatted)
        if entry_widget: entry_widget.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Execution Error", str(e))

def select_file(entry_widget):
    file_path = filedialog.askopenfilename(filetypes=[("Android Files", "*.zip *.apk"), ("All files", "*.*")])
    if file_path:
        file_path = file_path.strip("'").strip('"')
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, file_path)

def execute_payload(path_entry):
    path = path_entry.get().strip("'").strip('"')
    if not path or not os.path.exists(path):
        messagebox.showerror("File Error", "Select a valid file first.")
        return
    
    ext = os.path.splitext(path)[1].lower()
    if ext == ".zip":
        run_cmd(f"adb sideload {path}")
    elif ext == ".apk":
        run_cmd(f"adb install -r {path}")
    else:
        run_cmd(f"adb push {path} /sdcard/Download/")

init_db()
root = tk.Tk()
root.title("Advanced ADB Core")
root.geometry("500x650")
root.configure(bg="#121212")

tk.Label(root, text="DEVICE CONTROL", bg="#121212", fg="#00ff00", font=("Courier", 11, "bold")).pack(pady=10)

# Power Buttons
btn_frame = tk.Frame(root, bg="#121212")
btn_frame.pack(fill="x", padx=30)
tk.Button(btn_frame, text="BOOTLOADER", bg="#333333", fg="#00ff00", width=15, command=lambda: run_cmd("adb reboot bootloader")).pack(side="left", pady=2)
tk.Button(btn_frame, text="FASTBOOT D", bg="#333333", fg="#00ff00", width=15, command=lambda: run_cmd("adb reboot fastboot")).pack(side="right", pady=2)

# Payload Section
tk.Frame(root, height=2, bd=1, relief="sunken", bg="#00ff00").pack(fill="x", padx=30, pady=15)
tk.Label(root, text="INSTALLER / SIDELOADER", bg="#121212", fg="#00ff00", font=("Courier", 10, "bold")).pack()

path_frame = tk.Frame(root, bg="#121212")
path_frame.pack(fill="x", padx=30, pady=5)
file_entry = tk.Entry(path_frame, bg="#222222", fg="#00ff00", font=("Courier", 9))
file_entry.pack(side="left", expand=True, fill="x", padx=(0, 5))
tk.Button(path_frame, text="BROWSE", bg="#444444", fg="white", font=("Courier", 8), command=lambda: select_file(file_entry)).pack(side="right")

tk.Button(root, text="⚡ EXECUTE PAYLOAD ⚡", bg="#005500", fg="white", font=("Courier", 10, "bold"), command=lambda: execute_payload(file_entry)).pack(fill="x", padx=30, pady=10)

# Manual Entry
tk.Label(root, text="MANUAL COMMAND", bg="#121212", fg="#00ff00", font=("Courier", 10)).pack(pady=10)
cmd_entry = tk.Entry(root, bg="#222222", fg="#00ff00", font=("Courier", 10))
cmd_entry.pack(fill="x", padx=30, pady=5)
cmd_entry.bind('<Return>', lambda e: run_cmd(cmd_entry.get(), cmd_entry))
tk.Button(root, text="EXECUTE", bg="#0055ff", fg="white", font=("Courier", 9, "bold"), command=lambda: run_cmd(cmd_entry.get(), cmd_entry)).pack(pady=5)

root.mainloop()
