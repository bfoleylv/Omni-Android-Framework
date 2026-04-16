import os, subprocess
from tkinter import messagebox
print("[*] Accessing Root Contacts Database...")
# ADB command to pull the contacts database from a rooted device
cmd = "adb shell su -c 'cp /data/data/com.android.providers.contacts/databases/contacts2.db /sdcard/ && chmod 666 /sdcard/contacts2.db' && adb pull /sdcard/contacts2.db ./backup_contacts.db"
messagebox.showinfo("Omni-Source", "Pulling Contacts Database via Root...")
