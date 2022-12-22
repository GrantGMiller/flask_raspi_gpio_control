import random
import sys

if sys.platform.startswith('linux'):
    from .macro_helper import *
else:
    from macro_helper import *


# chase lights left to right


def get_macro():
    m = Macro()
    delay = random.random() * 0.25
    m.all_off()
    for i in range(random.randint(20, 30)):
        for index, pin in enumerate(ALL_PINS):
            if i % 3 == index % 3:
                m.on(pin)
            else:
                m.off(pin)

        m.sleep(delay)

    m.all_off()
    m.sleep(1)
    m.all_on()
    return m
