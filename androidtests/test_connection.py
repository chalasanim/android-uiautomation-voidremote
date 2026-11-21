from voidremote import VoidRemote
import time, subprocess, xml.etree.ElementTree as ET
from androidtests.helpers import get_text


def test_connection_disconnected():
    client = VoidRemote()
    client.start()

    device = client.devices().first()

    device.shell("am start -n com.pusun.pusunintelligence/.activity.SplashActivity")
    time.sleep(3)

    #dump the ui

    status = get_text(device, "com.pusun.pusunintelligence:id/connect")

    print("Status:", status)
    assert status == "Disconnected"
    client.close()

