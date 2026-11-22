from voidremote import VoidRemote
from androidtests.helpers import launch_app, tap, wait_for_element, get_text, RID


def test_navigation_tabs():
    client = VoidRemote()
    client.start()
    device = client.devices().first()

    try:
        launch_app(device)

        for tab_rid, label in [
            (RID["device_tab"],   "Device"),
            (RID["training_tab"], "Training"),
            (RID["mine_tab"],     "Mine"),
            (RID["home_tab"],     "Home"),
        ]:
            tap(device, tab_rid)
            # after each tap, HOME tab should still exist (app didn't crash)
            wait_for_element(device, RID["start"], timeout=10)
            print(f"navigated to {label}")

    finally:
        client.close()