from index import Run
from bootinfo import Service
from configuration import ServiceConfiguration
from streams import ReadStream, WriteStream
from loguru import logger
import time
import signal
import rovercom
import zmq
from testing import inject_valid_service



def run(service : Service, configuration : ServiceConfiguration):
    ######################################################

    context = zmq.Context()

    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:8829")


    while True:
        tuning = rovercom.TuningState(timestamp=int(time.time() * 1000), dynamic_parameters=[
            rovercom.TuningStateParameter(number=rovercom.TuningStateParameterNumberParameter(key="max-iterations",value=5))
            ]
        ).SerializeToString()



        socket.send(tuning)







def onTerminate(sig : signal):
    logger.info("Terminating")
    return None




inject_valid_service()


Run(run, onTerminate)
