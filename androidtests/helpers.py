import time, subprocess
import xml.etree.ElementTree as ET

PACKAGE = "com.pusun.pusunintelligence/"
Activity = ".activity.SplashActivity"

# resource-ids that matter
RID = {
    "connect":     f"{PACKAGE}:id/connect",
    "signal_note": f"{PACKAGE}:id/signal_note",
    "single_test": f"{PACKAGE}:id/test",
    "start":       f"{PACKAGE}:id/btn_start",
    "save":        f"{PACKAGE}:id/btn_save",
    "speed_value": f"{PACKAGE}:id/su_tv",
    "angle_value": f"{PACKAGE}:id/jiao_tv",
    "ball":        f"{PACKAGE}:id/ball",
    "home_tab":    f"{PACKAGE}:id/info_check",
    "device_tab":  f"{PACKAGE}:id/train_check",
    "training_tab":f"{PACKAGE}:id/share_check",
    "mine_tab":    f"{PACKAGE}:id/mine_manage",
}

# ---------- low-level UI dump ----------

def _dump(device):
    device.shell("rm -f /sdcard/ui.xml")
    device.shell("uiautomator dump /sdcard/ui.xml")
    time.sleep(2)
    subprocess.run(["adb", "pull", "/sdcard/ui.xml", "ui.xml"],
                   check=True, capture_output=True)
    return ET.parse("ui.xml").getroot()


def _parse_bounds(node):
    b = node.get("bounds")
    if not b:
        return None
    x1, y1, x2, y2 = map(int, b.replace("][", ",").strip("[]").split(","))
    return (x1, y1, x2, y2)

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

def wait_for_text(device, resource_id, expected, timeout=15, interval=1):
    end = time.time() + timeout
    while time.time() < end:
        t = get_text(device, resource_id)
        if t == expected:
            return t
        time.sleep(interval)
    raise TimeoutError(
        f"{resource_id} never became {expected!r} (last value: {t!r})"
    )


def tap(device, resource_id):
    centre = get_centre(device, resource_id)
    if c is None:
        raise LookupError(f"Can not tap, {resource_id} is not found")
    device.shell(f"Input tap {c[0]} c{[1]}")
    time.sleep(1)
    
def find_element(device, resource_id):
    for node in _dump(device).iter("node"):
        if node.get("resource-id") == resource_id :
            return node
    return None

def get_centre(device,resource_id):
    node = find_element(device, resource_id)
    if node is None:
        return None
    b = _parse_bounds(node)
    if not b :
        return None
    x1, x2, y1, y2 = b
    return ((x1+x2)//2, (y1+y2)//2)

def tap_text(device, text):
    for node in _dump(device).iter("node"):
        if node.get("text") == text:
            b = _parse_bounds(node)
            if b:
                x1, y1, x2, y2 = b
                device.shell(f"input tap {(x1+x2)//2} {(y1+y2)//2}")
                time.sleep(1)
                return
    raise LookupError(f"cannot tap text {text!r}: not found")


def type_text(device, text):
    # `input text` needs spaces escaped as %s
    device.shell(f'input text "{text.replace(" ", "%s")}"')
    time.sleep(0.5)


def swipe(device, x1, y1, x2, y2, ms=300):
    device.shell(f"input swipe {x1} {y1} {x2} {y2} {ms}")
    time.sleep(1)


def key(device, keycode):
    device.shell(f"input keyevent {keycode}")
    time.sleep(0.5)

def force_stop_app(device):
    device.shell(f"am force-stop {PACKAGE}")
    
def take_screenshot(device, sname = 'screen.png'):
    device.screenshot(sname)
    return sname

