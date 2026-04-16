import os, subprocess
from tkinter import messagebox
print("[*] Starting Full System Partition Backup...")
# Uses tar to compress the data folder while maintaining permissions
cmd = "adb shell su -c 'tar -cvf /sdcard/full_backup.tar /data' && adb pull /sdcard/full_backup.tar ./"
messagebox.showinfo("Omni-Source", "Full Root Backup initiated. This may take a while...")
