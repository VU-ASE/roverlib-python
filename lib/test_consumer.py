from roverlib.src import roverlib

r = roverlib.init()

while True:
    data_stream = r.subscribe("producer", "data")
    msg = data_stream.read()

    r.log(f"MSG: {msg}")

    r.print_info()
