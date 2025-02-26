from index import Run
from bootinfo import Service
from configuration import ServiceConfiguration
from streams import ReadStream, WriteStream
from loguru import logger
import time
import signal
import rovercom
from testing import inject_valid_service


def run(service : Service, configuration : ServiceConfiguration):
    time.sleep(1000)

    speed, err = configuration.GetFloatSafe("speed")
    logger.info(speed)

    configuration._setString("speed", 1)

    speed, err = configuration.GetFloatSafe("speed")
    logger.info(speed)
    logger.error(err)

    ll, err = configuration.GetStringSafe("log-level")
    logger.info(ll)
    logger.error(err)

    maxIt, err = configuration.GetFloat("max-iterations")
    logger.info(maxIt)
    logger.error(err)

    ######################################################

    wr : WriteStream = service.GetWriteStream("motor_movement")

    logger.critical(wr.stream.address)   
    


    return None

    while True:
        err = wr.Write(
            rovercom.SensorOutput(
                sensor_id=2,
                timestamp=int(time.time() * 1000),
                controller_output=rovercom.ControllerOutput(
                    steering_angle=float(1),
                    left_throttle=float(speed),
                    right_throttle=float(speed),
                    front_lights=False
                ),
            ) 
        )
        logger.error(err)
    logger.debug("done1")

    


    logger.critical(err)

    logger.info(wr)

    logger.info(err)

    
def onTerminate(sig : signal):
    logger.info("Terminating")
    return None




inject_valid_service()


Run(run, onTerminate)
