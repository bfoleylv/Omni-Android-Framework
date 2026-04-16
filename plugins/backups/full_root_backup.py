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
        # Force real-time output and combined error logging
        cmd = f"adb shell su -c 'tar -cvf /sdcard/temp_backup.tar /data' && adb pull /sdcard/temp_backup.tar \"{target_file}\" && adb shell rm /sdcard/temp_backup.tar"
        
        progress_text.insert(tk.END, f"[*] EXECUTING: {cmd}\n\n")
        
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        has_output = False
        for line in process.stdout:
            has_output = True
            progress_text.insert(tk.END, line)
            progress_text.see(tk.END)
            win.update_idletasks()
        
        process.wait()
        
        if not has_output:
            progress_text.insert(tk.END, "\n[!] ERROR: No data received. Check ADB and Root permissions.")
        else:
            messagebox.showinfo("SUCCESS", f"Backup Finished!\nLocation: {target_file}")
            win.destroy()

    win.after(500, start_stream)
    win.mainloop()

if __name__ == "__main__":
    run_backup()
