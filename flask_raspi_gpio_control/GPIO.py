pinStates = {}

ALL_PIN_NUMBERS = [14, 15, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21, 2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26]

IN = 0
OUT = 1
HIGH = 1
LOW = 0

BCM = 'BCM'


def setmode(mode):
    pass


def setwarnings(state):
    pass


def setup(pin, mode, initial=None):
    pass


def output(pin, state):
    assert isinstance(pin, int) and isinstance(state, int)
    oldState = pinStates.get(pin, 0)
    if oldState != state:
        print('Pin {} changed to {}'.format(pin, state))
    pinStates[pin] = state
