import datetime
import random
import time
import requests
import sys
import config
import threading

if sys.platform.startswith('linux'):
    from . import gpio_helper as GPIO
    from . import macro_1 as m1
    from . import macro_2 as m2
    from . import macro_3 as m3
    from . import macro_4 as m4
else:
    # macos windows
    import gpio_helper as GPIO
    import macro_1 as m1
    import macro_2 as m2
    import macro_3 as m3
    import macro_4 as m4

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


def all_off():
    for pin in ALL_OUTPUT_PIN_NUMBERS:
        GPIO.output(int(pin), 0)


go = True


def Slack(*args):
    if config.SLACK_URL:
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


Slack('starting 2022-12-18 6:32pm')

numErrors = 0


def check_button_push_event():
    print('check', datetime.datetime.now())
    # return True if button was pushed
    if GPIO.input(PIN_BUTTON) == GPIO.LOW:
        Slack('button pushed, triggering callback')
        print('eventCallbacks=', eventCallbacks)
        BlinkAllLights(3)

        if PIN_BUTTON in eventCallbacks:
            # other scripts can use RegisterCallback to make things happen when pins go high/low
            eventCallbacks[PIN_BUTTON](GPIO.input(PIN_BUTTON))

        return True


def Start(): # dont rename, there are other systems depending on this name
    while go:
        now = datetime.datetime.now()
        end_test_date = datetime.date(year=2022, month=12, day=19)
        if now.hour >= 17 or now.hour < 7 or now.date() <= end_test_date:
            # night
            all_on()
            all_macros = [m1, m2, m3, m4]

            macro = random.choice(all_macros).get_macro()
            do_macro(macro)
        else:
            # day
            all_off()

        time.sleep(random.randint(10, 30))


def do_macro(macro):
    for action in macro.actions:
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


def Stop():
    print('Stop()')
    global go
    go = False


eventCallbacks = {}


def RegisterEvent(pin, callback):
    eventCallbacks[pin] = callback


def thread_loop():
    while go:
        time.sleep(1)
        check_button_push_event()


loop_thread = threading.Thread(target=thread_loop)
loop_thread.start()

if __name__ == '__main__':
    # another process calls .Start(), so put whatever u want into def Start()
    Start()
