import time
import requests
import sys

ALL_OUTPUT_PIN_NUMBERS = [16, 20, 21, 5, 6, 13, 19, 26]
PIN_BUTTON = 12

if sys.platform.startswith('win'):
    BASE_URL = 'http://192.168.68.105:5000/'
    import GPIO


else:  # linux
    BASE_URL = 'http://192.168.68.105:5000/'
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(True)

for pinName in ALL_OUTPUT_PIN_NUMBERS:
    GPIO.setup(int(pinName), GPIO.OUT)

GPIO.setup(PIN_BUTTON, GPIO.IN)


def BlinkAllLights(numberOfBlinks=1):
    for i in range(numberOfBlinks * 2):
        for pin in ALL_OUTPUT_PIN_NUMBERS:
            GPIO.output(pin, 1)
        time.sleep(0.2)
        for pin in ALL_OUTPUT_PIN_NUMBERS:
            GPIO.output(pin, 0)
        time.sleep(0.2)


BlinkAllLights(25)


def Start():
    print('starting while loop')
    totalRequests = 0
    startTime = time.time()
    while True:
        totalRequests += 1
        resp = requests.get(BASE_URL)
        print('resp.text=', resp.text)
        for pinNumberStr, state in resp.json().items():
            GPIO.output(
                int(pinNumberStr),
                {'On': 0, 'Off': 1}.get(state)
            )

        print('Average req/second=', round(totalRequests / (time.time() - startTime), 2))
        if sys.platform.startswith('win'):
            time.sleep(1)
        else:
            # with no delay, raspi was able to send 5 request per second to local webserver
            time.sleep(1)

        if GPIO.input(PIN_BUTTON) == GPIO.LOW:
            BlinkAllLights(25)


if __name__ == '__main__':
    Start()
