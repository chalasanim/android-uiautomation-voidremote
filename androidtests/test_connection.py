from voidremote import VoidRemote
from androidtests.helpers import get_text, launch_App


def test_connection_disconnected():
    client = VoidRemote()
    client.start()

    device = client.devices().first()

    launch_App(device)

    #dump the ui

    status = get_text(device, "com.pusun.pusunintelligence:id/connect")

    print("Status:", status)
    assert status == "Disconnected"
    client.close()

