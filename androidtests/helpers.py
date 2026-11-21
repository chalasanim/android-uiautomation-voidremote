import time, subprocess
import xml.etree.ElementTree as ET

PACKAGE = "com.pusun.pusunintelligence/"
Activity = ".activity.SplashActivity"

def launch_App(device, wait = 5):
    device.shell(f"am start -n", {PACKAGE}/{Activity})

def get_text(device,resource_id):
    device.shell("ui automator dump /sdcard/ui.xml")
    time.sleep(3)
    subprocess.run(["adb", "pull", "/sdcard/ui.xml", "ui.xml"], check=True, capture_output=True)
    tree = ET.parse("ui.xml")
    status = None
    for node in tree.getroot().iter("node"):
        if node.get("resource-id") == resource_id:
            return node.get("text")
            break
    return None