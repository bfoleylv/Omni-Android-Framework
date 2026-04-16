import subprocess, os, requests
LOG = "/home/bfoleylv/.logs/android_toolkit.log"
URL = "YOUR_DISCORD_WEBHOOK"
def _err(a, e):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "a") as f: f.write(f"{a}: {e}
")
    if input(f"{a} failed. Send report? (y/n): ").lower() == "y":
        requests.post(URL, json={"content": f"**Core Error**
{a}: {e}"})
def sideload(p):
    try:
        r = subprocess.run(["adb", "install", "-r", p], capture_output=True, text=True, check=True)
        return r.stdout
    except Exception as e: _err("sideload", str(e))
def fastboot():
    try: subprocess.run(["adb", "reboot", "bootloader"], check=True)
    except Exception as e: _err("fastboot", str(e))
def recovery():
    try: subprocess.run(["adb", "reboot", "recovery"], check=True)
    except Exception as e: _err("recovery", str(e))
