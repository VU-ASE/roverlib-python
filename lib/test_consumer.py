from roverlib.src import roverlib

r = roverlib.init()

r.print_info()


while True:
    socket = r.input_handles["python-producer_data"]
    msg = socket.recv()
    print(f"MSG: {msg}")
