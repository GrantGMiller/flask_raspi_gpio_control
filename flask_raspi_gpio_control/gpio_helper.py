import sys
from collections import defaultdict

if sys.platform.startswith('win') or sys.platform.startswith('darwin'):
     import GPIO


else:  # linux
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(True)

OUT = GPIO.OUT
IN = GPIO.IN
PUD_UP = GPIO.PUD_UP
HIGH = GPIO.HIGH
LOW = GPIO.LOW

global pinSates
pinSates = defaultdict(lambda: 0)


def setup(pinNum, state, **k):
    pinNum = int(pinNum)

    GPIO.setup(pinNum, state, **k)


def input(pinNum):
    return GPIO.input(int(pinNum))


def output(pinNum, state):
    global pinStates
    pinNum = int(pinNum)
    pinSates[pinNum] = state
    GPIO.output(pinNum, state)


def read(pinNum):
    pinNum = int(pinNum)
    return pinSates[pinNum]
