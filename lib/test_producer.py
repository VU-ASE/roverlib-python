from roverlib.src import roverlib

import time
import pickle

r = roverlib.init()

r.print_info()


lux_sensor = roverlib.SensorOutput(
    sensor_id=34, timestamp=0, status=0, lux_output=roverlib.LuxSensorOutput(lux=69)
)
lux_stream = r.publish("brightness")

my_var = 0
my_var_stream = r.publish("data")

while True:
    increment = r.options["increment"]

    my_var = my_var + increment
    lux_sensor.lux_output.lux = lux_sensor.lux_output.lux + increment

    serialized_var = pickle.dumps(my_var)
    serialized_lux = bytes(lux_sensor)

    my_var_stream.write(serialized_var)
    lux_stream.write(serialized_lux)

    time.sleep(1)
