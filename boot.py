import storage
import usb_cdc

# Hide the CIRCUITPY drive for end users while keeping the serial REPL
# available for updater tools.
storage.disable_usb_drive()
usb_cdc.enable(console=True, data=False)
