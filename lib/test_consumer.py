from roverlib.src import roverlib
import time

import pickle

r = roverlib.init()


data_stream = r.subscribe("producer", "data")
brightness_stream = r.subscribe("producer", "brightness")

while True:


    # read() and write() - only one of the RoverOutput types
    # read_raw() and write_raw() - only sends and receives bytes

    data_bytes = data_stream.read()
    brighness_bytes = brightness_stream.read()

    data = pickle.load()

    brightness = roverlib.SensorOutput().FromString(brightness_stream.read())

    r.log(f"DATA: {data}, BRIGHTNESS: {brightness}")

    time.sleep(1)
