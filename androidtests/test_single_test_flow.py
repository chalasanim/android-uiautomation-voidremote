from voidremote import VoidRemote
import time
from androidtests.helpers import (
                                    launch_App, take_screenshot, tap, wait_for_text, force_stop_app, get_text, RID
)


def single_test_flow():

    client = VoidRemote()
    client.start()
    device = client.devices().first()

    try :
        # 1--clean start 

        force_stop_app(device)
        launch_App(device)

        #2-- Check conection status
        assert get_text(device, RID["connect"]) == "Disconnected"

        # --- 3. capture baseline ---
        speed_before = get_text(device, RID["speed_value"])
        ball_before  = get_text(device, RID["ball"])
        print(f"before: speed={speed_before} ball={ball_before}")
        assert speed_before == "43", f"unexpected speed: {speed_before}"
        assert ball_before == "1",  f"unexpected ball: {ball_before}"

        # --- 4. the flow under test ---
        tap(device, RID["single_test"])
        tap(device, RID["start"])

        # the START button may disappear while the test runs — wait for it to come back
        wait_for_text(device, RID["start"], "START", timeout=30)

        tap(device, RID["save"])

        # --- 5. post-conditions ---
        ball_after = get_text(device, RID["ball"])
        print(f"after: ball={ball_after}")
        assert ball_after is not None, "ball counter missing after save"

    except Exception as e:
        name = take_screenshot(device, f"failure_{int(time.time())}.png")
        print(f"[FAILED] {e} — screenshot: {name}")
        raise

    finally:
        client.close()


