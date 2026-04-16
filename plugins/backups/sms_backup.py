import os, subprocess
from tkinter import messagebox
print("[*] Extracting SMS/MMS History...")
# Command to grab the SMS database
cmd = "adb shell su -c 'cp /data/data/com.android.providers.telephony/databases/mmssms.db /sdcard/ && chmod 666 /sdcard/mmssms.db' && adb pull /sdcard/mmssms.db ./backup_sms.db"
messagebox.showinfo("Omni-Source", "Pulling SMS Database via Root...")
