import json

PIN_6 = 16
PIN_7 = 20
PIN_8 = 21
PIN_1 = 5
PIN_2 = 6
PIN_3 = 13
PIN_4 = 19
PIN_5 = 26

ALL_PINS = [
    PIN_1, PIN_2, PIN_3, PIN_4, PIN_5, PIN_6, PIN_7, PIN_8
]


class Macro:
    def __init__(self):
        self.actions = []

    def on(self, pinNum):
        self.actions.append((pinNum, 'On'))

    def off(self, pinNum):
        self.actions.append((pinNum, 'Off'))

    def toggle(self, pinNum):
        self.actions.append((pinNum, 'Toggle'))

    def sleep(self, seconds):
        self.actions.append(('Sleep', seconds))

    def all_on(self):
        for pin in ALL_PINS:
            self.on(pin)

    def all_off(self):
        for pin in ALL_PINS:
            self.off(pin)

    def all_toggle(self):
        for pin in ALL_PINS:
            self.toggle(pin)

    def json(self):
        return json.dumps({'actions':self.actions}, indent=2)