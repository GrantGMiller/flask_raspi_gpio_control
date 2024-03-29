import random
import sys

if sys.platform.startswith('linux'):
    from .macro_helper import *
else:
    from macro_helper import *

# all lights shimmer

def get_macro():

    m = Macro()

    for i in range(5000):
        m.toggle(random.choice(ALL_PINS))
        m.sleep(random.random()/1000)

    m.all_on()

    return m
