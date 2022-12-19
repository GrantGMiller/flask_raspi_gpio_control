import random
import sys

if sys.platform.startswith('linux'):
    from .macro_helper import *
else:
    from macro_helper import *

# twinkle left to right

sleepTime = random.random() / 5

m = Macro()

for i in range(10000):
    m.toggle(random.choice(ALL_PINS))
    m.sleep(random.random()/1000)

m.all_on()

