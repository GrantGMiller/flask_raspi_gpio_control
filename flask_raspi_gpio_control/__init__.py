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

GPIO.setup(PIN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def BlinkAllLights(numberOfBlinks=1):
    DELAY = 0.1
    print('BlinkAllLights(', numberOfBlinks)
    for i in range(numberOfBlinks * 2):
        for pin in ALL_OUTPUT_PIN_NUMBERS:
            GPIO.output(pin, 1)
        time.sleep(DELAY)
        for pin in ALL_OUTPUT_PIN_NUMBERS:
            GPIO.output(pin, 0)
        time.sleep(DELAY)


go = True


def Start():
    print('starting while loop')
    BlinkAllLights(7)
    totalRequests = 0
    startTime = time.time()
    while go is True:
        try:
            totalRequests += 1
            resp = requests.get(BASE_URL)
            print('resp.text=', resp.text)
            for pinNumberStr, state in resp.json().items():
                GPIO.output(
                    int(pinNumberStr),
                    {'On': GPIO.LOW, 'Off': GPIO.HIGH}.get(state)
                )

            print('Average req/second=', round(totalRequests / (time.time() - startTime), 2))
        except Exception as e:
            print(e)
            # reset the measurements
            totalRequests = 0
            startTime = time.time()

        if sys.platform.startswith('win'):
            time.sleep(1)
        else:
            # with no delay, raspi was able to send 5 request per second to local webserver
            time.sleep(1)

        if GPIO.input(PIN_BUTTON) == GPIO.LOW:
            print('eventCallbacks=', eventCallbacks)
            BlinkAllLights(5)
            if PIN_BUTTON in eventCallbacks:
                eventCallbacks[PIN_BUTTON](GPIO.input(PIN_BUTTON))


def Stop():
    print('Stop()')
    global go
    go = False


eventCallbacks = {}


def RegisterEvent(pin, callback):
    eventCallbacks[pin] = callback


if __name__ == '__main__':
    Start()
