import sys
import random

if sys.platform.startswith('linux'):
    from .macro_helper import *
else:
    from macro_helper import *

# twinkle left to right
sleepTime = random.random() / 5

m = Macro()
lastPin = None
for pin in ALL_PINS:
    if lastPin:
        m.toggle(lastPin)
    m.toggle(pin)
    m.sleep(sleepTime)

    lastPin = pin

m.toggle(pin)

