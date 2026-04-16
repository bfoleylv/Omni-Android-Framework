import subprocess
subprocess.run("echo 'SUBSYSTEM==\"usb\", ATTR{idVendor}==\"*\", MODE=\"0666\", GROUP=\"plugdev\"' | sudo tee /etc/udev/rules.d/51-android.rules && sudo udevadm control --reload-rules", shell=True)
print("USB Rules Fixed!")
