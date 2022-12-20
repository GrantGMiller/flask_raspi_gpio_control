import random
import sys

if sys.platform.startswith('linux'):
    from .macro_helper import *
else:
    from macro_helper import *


# move one light back and forth a few times


def get_macro():
    m = Macro()
    delay = random.random() * 0.5
    m.all_off()
    for i in range(random.randint(5, 10)):
        direction = i % 2
        if direction:
            for pin in len(ALL_PINS):
                m.all_off()
                m.on(pin)
                m.sleep(delay)
        else:
            for pin in reversed(ALL_PINS):
                m.all_off()
                m.on(pin)
                m.sleep(delay)

    m.all_off()
    m.sleep(1)
    m.all_on()
    return m
