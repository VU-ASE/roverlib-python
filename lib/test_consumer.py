from roverlib.src import roverlib

r = roverlib.init()


while True:
    msg = r.subscribe("python-producer_data")
    r.log(f"MSG: {msg}")
