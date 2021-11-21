import time
import requests
import sys
import config

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
    for i in range(numberOfBlinks):
        for pin in ALL_OUTPUT_PIN_NUMBERS:
            GPIO.output(pin, 1)
        time.sleep(DELAY)
        for pin in ALL_OUTPUT_PIN_NUMBERS:
            GPIO.output(pin, 0)
        time.sleep(DELAY)


go = True


def Slack(*args):
    resp = requests.post(
        url=config.SLACK_URL,
        json={
            'text': '{}: {}'.format(
                sys.platform,
                ' '.join(str(a) for a in args)
            )
        }
    )
    print('Slack resp=', resp.text)


Slack('starting', '627')


def Start():
    print('starting while loop')
    BlinkAllLights(2)
    totalRequests = 0
    startTime = time.time()
    while go is True:
        try:
            totalRequests += 1
            resp = requests.get(
                BASE_URL + 'lights',
                params={'apiKey': 'MillerTime5625475311!'},
                timeout=2
            )
            print('resp.text=', resp.text)
            for pinNumberStr, state in resp.json().items():
                if int(pinNumberStr) in ALL_OUTPUT_PIN_NUMBERS:
                    GPIO.output(
                        int(pinNumberStr),
                        {'On': GPIO.HIGH, 'Off': GPIO.LOW}.get(state)
                    )

            print('Average req/second=', round(totalRequests / (time.time() - startTime), 2))
            delay = resp.json().get('delay', 1)

        except Exception as e:
            print(e)
            # reset the measurements
            totalRequests = 0
            startTime = time.time()
            delay = 1

        time.sleep(delay)

        if GPIO.input(PIN_BUTTON) == GPIO.LOW:
            Slack('button pushed, triggering callback')
            print('eventCallbacks=', eventCallbacks)
            BlinkAllLights(3)
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
