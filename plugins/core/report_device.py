import subprocess
import webbrowser
import urllib.parse
import tkinter as tk
from tkinter import messagebox

def report_to_community():
    # 1. Initialize hidden root for popups
    root = tk.Tk()
    root.withdraw()

    try:
        # 2. Scrape device properties
        model = subprocess.run(['adb', 'shell', 'getprop', 'ro.product.model'], capture_output=True, text=True).stdout.strip()
        version = subprocess.run(['adb', 'shell', 'getprop', 'ro.build.display.id'], capture_output=True, text=True).stdout.strip()
        kernel = subprocess.run(['adb', 'shell', 'uname', '-r'], capture_output=True, text=True).stdout.strip()
        
        if not model:
            raise Exception("No device found")

        # 3. The Disclaimer / User Consent
        msg = (f"DEVICE FOUND\n"
               f"---------------------------\n"
               f"Model: {model}\n"
               f"Build: {version}\n"
               f"Kernel: {kernel}\n\n"
               f"Would you like to submit these specs to the community database?\n"
               f"This opens a browser to create a GitHub Issue.")
        
        if messagebox.askyesno("Community Contribution", msg):
            # 4. Format the GitHub URL
            # NOTE: Update the URL below with your actual GitHub username once you create the repo!
            repo_url = "https://github.com/YOUR_USERNAME/Omni-Android-Framework/issues/new"
            title = f"[Device Report] {model}"
            body = (f"### Device Compatibility Report\n"
                    f"- **Model:** {model}\n"
                    f"- **Build ID:** {version}\n"
                    f"- **Kernel Version:** {kernel}\n"
                    f"- **Status:** Verified with Omni-Framework")
            
            params = {
                "title": title,
                "body": body,
                "labels": "device-report"
            }
            
            full_url = f"{repo_url}?{urllib.parse.urlencode(params)}"
            webbrowser.open(full_url)
            print(f"Opening browser for {model}...")
            
    except Exception as e:
        messagebox.showerror("Connection Error", "Could not find an ADB device. Please check your USB connection.")
    
    root.destroy()

if __name__ == "__main__":
    report_to_community()
