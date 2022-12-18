import time
import requests
import sys
import config
from . import gpio_helper as GPIO

ALL_OUTPUT_PIN_NUMBERS = [16, 20, 21, 5, 6, 13, 19, 26]
PIN_BUTTON = 12
LEFT_TO_RIGHT = 'left to right'
RIGHT_TO_LEFT = 'right to left'
TOGGLE = 'Toggle'
SLEEP = 'Sleep'

if sys.platform.startswith('win'):
    # BASE_URL = 'http://localhost:5000/'
    BASE_URL = 'http://192.168.68.105:5000/'
    # BASE_URL = 'https://lights.grant-miller.com/'


else:  # linux
    BASE_URL = 'https://lights.grant-miller.com/'
    # BASE_URL = 'http://192.168.68.105:5000/'

for pinNum in ALL_OUTPUT_PIN_NUMBERS:
    GPIO.setup(pinNum, GPIO.OUT)

GPIO.setup(PIN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def BlinkAllLights(numberOfBlinks=1):
    DELAY = 0.1
    print('BlinkAllLights(', numberOfBlinks)

    for i in range(numberOfBlinks):
        for pin in ALL_OUTPUT_PIN_NUMBERS:
            GPIO.output(int(pin), 1)
        time.sleep(DELAY)

        for pin in ALL_OUTPUT_PIN_NUMBERS:
            GPIO.output(int(pin), 0)
        time.sleep(DELAY)

def all_on():
    for pin in ALL_OUTPUT_PIN_NUMBERS:
        GPIO.output(int(pin), 1)

go = True


def Slack(*args):
    if not sys.platform.startswith('win'):
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


Slack('starting')

numErrors = 0


def Start():
    print('starting while loop')
    global numErrors

    BlinkAllLights(2)
    totalRequests = 0
    startTime = time.time()
    while go is True:
        try:
            totalRequests += 1
            resp = requests.get(
                BASE_URL + 'lights',
                params={'apiKey': config.API_KEY},
                timeout=2
            )
            print('resp.text=', resp.text)
            for pinNumberStr, state in resp.json().items():
                if pinNumberStr.isdigit() and int(pinNumberStr) in ALL_OUTPUT_PIN_NUMBERS:
                    GPIO.output(
                        int(pinNumberStr),
                        {'On': GPIO.HIGH, 'Off': GPIO.LOW}.get(state)
                    )

            for macro in resp.json().get('macros', []):
                for action in macro.get('actions', []):
                    print('93 action=', action)
                    if str(action[0]).isdigit() and int(action[0]) in ALL_OUTPUT_PIN_NUMBERS:
                        pinNum = action[0]
                        action = action[1]
                        GPIO.output(
                            int(pinNum),
                            {
                                'On': GPIO.HIGH,
                                'Off': GPIO.LOW,
                                'Toggle': GPIO.HIGH if GPIO.read(pinNum) == GPIO.LOW else GPIO.LOW,
                            }.get(action)
                        )

                    elif action[0] == SLEEP:
                        time.sleep(action[1])

            print('Average req/second=', round(totalRequests / (time.time() - startTime), 2))
            delay = resp.json().get('delay', 1)

        except Exception as e:
            numErrors += 1
            if numErrors <= 1:
                Slack(e)

            print(e)
            # reset the measurements
            totalRequests = 0
            startTime = time.time()
            delay = 10

            if sys.platform.startswith('win'):
                raise e

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
    all_on()
