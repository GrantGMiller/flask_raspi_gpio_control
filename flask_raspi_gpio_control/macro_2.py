from macro_helper import *

# twinkle left to right
m = Macro()
lastPin = None
for pin in ALL_PINS.reverse():
    if lastPin:
        m.toggle(lastPin)
    m.toggle(pin)
    m.sleep(0.1)

    lastPin = pin

m.toggle(pin)
