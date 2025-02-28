"""
Basic test
"""

import roverlib as rover
import time
import signal
from loguru import logger
import roverlib.rovercom as rovercom





def run(service : rover.Service, configuration : rover.ServiceConfiguration):
    time.sleep(1)

    speed = configuration.GetFloatSafe("speed")
    logger.info(speed)
    configuration._SetString("speed", 1)

    speed = configuration.GetFloatSafe("speed")
    logger.info(speed)
    
    ll = configuration.GetStringSafe("log-level")
    logger.info(ll)

    maxIt = configuration.GetFloat("max-iterations")
    logger.info(maxIt)

    ######################################################

    wr = service.GetWriteStream("motor_movement")
    rd = service.GetReadStream("imaging", "track_data")
    rd
    logger.critical(wr.stream.address)   
    
    rovercom.BatterySensorOutput





    # while True:
    #     err = wr.Write(
    #         rovercom.SensorOutput(
    #             sensor_id=2,
    #             timestamp=int(time.time() * 1000),
    #             controller_output=rovercom.ControllerOutput(
    #                 steering_angle=float(1),
    #                 left_throttle=float(speed),
    #                 right_throttle=float(speed),
    #                 front_lights=False
    #             ),
    #         ) 
    #     )
    #     logger.error(err)
    # logger.debug("done1")

    


    # logger.critical(err)

    # logger.info(wr)

    # logger.info(err)

    
def onTerminate(sig : signal):
    logger.info("Terminating")
    return None



rover.inject_valid_service()


rover.Run(run, onTerminate)


