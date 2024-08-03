from roverlib.src import roverlib

import time

r = roverlib.init()

while True:
    r.publish("data", b"yoooo")
    time.sleep(1)
