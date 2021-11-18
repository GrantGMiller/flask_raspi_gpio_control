import time
import requests
import sys

ALL_PIN_NUMBERS = [14, 15, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21, 2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26]

if sys.platform.startswith('win'):
    BASE_URL = 'http://192.168.68.105:5000/'
    import GPIO


else:  # linux
    BASE_URL = 'http://192.168.68.105:5000/'
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(True)

for pinName in ALL_PIN_NUMBERS:
    GPIO.setup(int(pinName), GPIO.OUT)


def Start():
    print('starting while loop')
    while True:
        resp = requests.get(BASE_URL)
        print('resp.text=', resp.text)
        for pinNumberStr, state in resp.json().items():
            GPIO.output(
                int(pinNumberStr),
                {'On': 0, 'Off': 1}.get(state)
            )
        time.sleep(1)


if __name__ == '__main__':
    Start()
