import importlib.util
import os

import storage
import usb_cdc

from keybow_hardware.pim551 import PIM551 as Hardware

RECOVERY_KEY_INDEX = 15
recovery_override = os.getenv("RECOVERY_KEY_INDEX")
if recovery_override:
    try:
        RECOVERY_KEY_INDEX = int(recovery_override)
    except ValueError:
        RECOVERY_KEY_INDEX = 15


def recovery_key_pressed():
    hardware = Hardware()
    if RECOVERY_KEY_INDEX < 0 or RECOVERY_KEY_INDEX >= hardware.num_keys():
        return False
    return bool(hardware.switch_state(RECOVERY_KEY_INDEX))


if recovery_key_pressed():
    storage.enable_usb_drive()
else:
    storage.disable_usb_drive()

usb_cdc.enable(console=True, data=True)

if importlib.util.find_spec("webusb"):
    import webusb

    webusb.set_enabled(True)
