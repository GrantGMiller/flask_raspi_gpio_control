import sys

if sys.platform.startswith('linux'):
    from .macro_helper import *
else:
    from macro_helper import *

# twinkle left to right
m = Macro()
lastPin = None
for pin in reversed(ALL_PINS):
    if lastPin:
        m.toggle(lastPin)
    m.toggle(pin)
    m.sleep(0.05)

    lastPin = pin

m.toggle(pin)

