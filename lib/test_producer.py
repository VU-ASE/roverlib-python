from roverlib.src import roverlib

import time

r = roverlib.init()

r.print_info()


while True:
    sock = r.output_handles["data"]

    time.sleep(1)

    sock.send(b"yoooo")
