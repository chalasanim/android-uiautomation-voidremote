import time, subprocess
import xml.etree.ElementTree as ET

PACKAGE = "com.pusun.pusunintelligence/"
Activity = ".activity.SplashActivity"

# element that only exists once the main screen is fully loaded
MAIN_READY_RID = f"{PACKAGE}:id/btn_start"

def launch_App(device, wait = 15):
    device.shell(f"am start -n", {PACKAGE}/{Activity})
    wait_for_element(device, MAIN_READY_RID,time_out=wait )

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

def wait_for_element( device, resource_id, time_out = 5, interval = 1) :
    # poll the ui elements until this resource id appears
    endtime = time.time() + time_out

    while time.time() <=  endtime :
        device.shell ("uiautomator  dump /sdcard/ui.xml")
        time.sleep(2)

        subprocess.run(["adb", "pull", "\sdcard\ui.xml","ui.xml"],
                       check=True, capture_output=True)
        tree = ET.parse("ui.xml")

        for node in tree.getroot().iter("node"):
            if node.get("resource-id") == "resource-id" :
                return node
        time.sleep(interval)
    raise TimeoutError(f"{resource_id} did not appear with time interval unit {interval}")

