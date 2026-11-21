from voidremote import VoidRemote
import time, subprocess, xml.etree.ElementTree as ET


def test_connection_disconnected():
    client = VoidRemote()
    client.start()

    device = client.devices().first()

    device.shell("am start -n com.pusun.pusunintelligence/.activity.SplashActivity")
    time.sleep(3)

    #dump the ui

    device.shell("ui automator dump /sdcard/ui.xml")
    time.sleep(3)
    subprocess.run(["adb", "pull", "/sdcard/ui.xml", "ui.xml"], check=True, capture_output=True)

    tree = ET.parse("ui.xml")
    status = None
    for node in tree.getroot().iter("node"):
        if node.get("resource-id") == "com.pusun.pusunintelligence:id/connect":
            status = node.get("text")
            break

    print("Status:", status)
    assert status == "Disconnected"
    client.close()

