from roverlib.src import roverlib

import time

r = roverlib.init()

r.print_info()

count = 0
out_stream = r.publish("data")

while True:
    out_stream.write(count)

    increment = r.options["increment"]
    count = count + increment
    time.sleep(1)
