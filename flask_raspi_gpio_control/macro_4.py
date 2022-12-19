import random
import sys

if sys.platform.startswith('linux'):
    from .macro_helper import *
else:
    from macro_helper import *


# every other light on/off a few times


def get_macro():
    m = Macro()
    delay = random.random()

    for i in range(random.randint(5, 10)):
        even = i % 2
        for index, pinNum in enumerate(ALL_PINS):
            if index % 2 == even:
                m.on(pinNum)
            else:
                m.off(pinNum)
        m.sleep(delay)

    m.all_on()
    return m
