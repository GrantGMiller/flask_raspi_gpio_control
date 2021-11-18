import time

import requests
import sys

if sys.platform.startswith('win'):
    BASE_URL = 'http://192.168.68.105:5000/'
else: #linux
    BASE_URL = 'http://192.168.68.105:5000/'


while True:
    resp = requests.get(BASE_URL)
    print('resp.text=', resp.text)
    time.sleep(1)