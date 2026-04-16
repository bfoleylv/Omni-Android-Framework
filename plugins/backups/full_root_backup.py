import os
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog

def run_backup():
    # 1. Hide root and ask for save location
    root_win = tk.Tk()
    root_win.withdraw()
    
    save_path = filedialog.asksaveasfilename(
        initialdir="/home/brandonfoley",
        title="Where should I save the Root Backup?",
        defaultextension=".tar",
        initialfile="oneplus8_root_data.tar"
    )

    if not save_path:
        return

    # 2. Status Window
    win = tk.Toplevel()
    win.title("ADB ROOT STATUS")
    win.geometry("400x200")
    win.configure(bg="#000000")
    
    lbl = tk.Label(win, text="COMMUNICATING WITH ONEPLUS 8...", bg="#000000", fg="#00ff00", font=("Courier", 10))
    lbl.pack(expand=True)
    win.update()

    try:
        # STEP A: Create the archive on the phone's internal storage
        # We use a simpler su command structure here
        print("[*] Creating archive on phone...")
        subprocess.run(["adb", "shell", "su", "-c", "tar -cvf /sdcard/backup_temp.tar /data"], check=True)
        
        # STEP B: Pull the file to your Kali machine
        print("[*] Pulling file to Kali...")
        subprocess.run(["adb", "pull", "/sdcard/backup_temp.tar", save_path], check=True)
        
        # STEP C: Cleanup
        print("[*] Cleaning up phone storage...")
        subprocess.run(["adb", "shell", "rm", "/sdcard/backup_temp.tar"], check=True)
        
        messagebox.showinfo("SUCCESS", f"Backup saved to:\n{save_path}")
        
    except subprocess.CalledProcessError as e:
        messagebox.showerror("ERROR", "Backup Failed.\n\nPossible reasons:\n1. Root was denied on phone screen.\n2. Phone storage is full.\n3. Cable disconnected.")
    
    win.destroy()

if __name__ == "__main__":
    run_backup()
