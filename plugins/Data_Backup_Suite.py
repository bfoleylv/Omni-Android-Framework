import subprocess
import os
from datetime import datetime

# --- SETTINGS ---
# All paths are strictly lowercase as requested
backup_dir = os.path.expanduser("~/android_backups")
os.makedirs(backup_dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

def backup_photos():
    print(f"--- Starting Photo Backup to {backup_dir} ---")
    subprocess.run(f"adb pull /sdcard/DCIM/Camera {backup_dir}/photos_{timestamp}", shell=True)
    print("Photos backup complete.")

def backup_contacts():
    print("--- Exporting Contacts ---")
    # Export to phone storage first
    subprocess.run("adb shell content query --uri content://contacts/phones --projection display_name:number > /sdcard/contacts_dump.txt", shell=True)
    # Pull to Kali
    subprocess.run(f"adb pull /sdcard/contacts_dump.txt {backup_dir}/contacts_{timestamp}.txt", shell=True)
    print("Contacts backup complete.")

def backup_sms():
    print("--- Pulling Text Messages ---")
    # This pulls the inbox database and formats it simply
    cmd = "adb shell content query --uri content://sms/inbox --projection address:body"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    with open(f"{backup_dir}/sms_inbox_{timestamp}.txt", "w") as f:
        f.write(result.stdout)
    print(f"SMS backup saved to {backup_dir}/sms_inbox_{timestamp}.txt")

if __name__ == "__main__":
    # When the button in your toolkit is pressed, it runs these:
    backup_photos()
    backup_contacts()
    backup_sms()
