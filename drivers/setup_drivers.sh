#!/bin/bash
echo "[*] Initializing Qualcomm & Samsung Support for Kali..."

# Path to the rules file we are about to create/update
RULE_FILE="/etc/udev/rules.d/51-android-common.rules"

# Qualcomm EDL Mode (9008) - Essential for unbricking
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="05c6", ATTR{idProduct}=="9008", MODE="0666", GROUP="plugdev"' | sudo tee $RULE_FILE

# Samsung Download Mode
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="04e8", MODE="0666", GROUP="plugdev"' | sudo tee -a $RULE_FILE

# Reload udev system to recognize the new IDs
sudo udevadm control --reload-rules
sudo udevadm trigger

# Load the kernel module for Qualcomm communication
sudo modprobe usbserial vendor=0x05c6 product=0x9008

echo "[+] Setup Complete. Qualcomm and Samsung devices are now authorized."
