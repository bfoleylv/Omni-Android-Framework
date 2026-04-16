import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

def run_backup():
    root_win = tk.Tk()
    root_win.withdraw()  
    
    target_file = filedialog.asksaveasfilename(
        initialdir="/home/brandonfoley",
        title="Select Backup Destination",
        defaultextension=".tar",
        initialfile="oneplus8_full_root.tar",
        filetypes=[("Tar files", "*.tar"), ("All files", "*.*")]
    )

    if not target_file:
        return 

    win = tk.Toplevel()
    win.title("ROOT BACKUP CONSOLE")
    win.geometry("700x450")
    win.configure(bg="#000000")

    progress_text = tk.Text(win, bg="#000000", fg="#00ff00", font=("Courier", 10))
    progress_text.pack(expand=True, fill="both", padx=10, pady=10)

    def start_stream():
        # Step 1: Verify Root Access first
        check_root = subprocess.run("adb shell su -c 'id'", shell=True, capture_output=True, text=True)
        
        if "root" not in check_root.stdout:
            progress_text.insert(tk.END, "[!] ROOT ACCESS DENIED\n")
            progress_text.insert(tk.END, "Check your OnePlus 8 screen and GRANT Magisk permissions.\n")
            return

        # Step 2: Run the actual backup
        cmd = f"adb shell su -c 'tar -cvf /sdcard/temp_backup.tar /data' && adb pull /sdcard/temp_backup.tar \"{target_file}\" && adb shell rm /sdcard/temp_backup.tar"
        
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        for line in process.stdout:
            progress_text.insert(tk.END, line)
            progress_text.see(tk.END)
            win.update_idletasks()
            
        messagebox.showinfo("SUCCESS", "Backup Complete!")
        win.destroy()

    win.after(500, start_stream)
    win.mainloop()
