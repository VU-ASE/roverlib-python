# roverlib-python
Building a service that runs on the rover? Then you'll need the roverlib. This is the variant for Python.

# Requirements

In order to use roverlib, you will need the following 3 requirements:

- pyzmq
- loguru
- betterproto

these can be installed by running:

```bash
pip install pyzmq loguru betterproto
```

# Installation

To install roverlib-python, simply run:

```bash
pip install roverlib
```

# Usage

After installation, you can use roverlib as follows:

```python
import roverlib
import signal
import time

def run(service : Service, configuration : ServiceConfiguration):
    speed, err = configuration.GetFloatSafe("speed")
    if err is not None:
        logger.error(err)

    name, err = configuration.GetStringSafe("name")
    if err is not None:
        logger.error(err)

    write_stream = service.GetWriteStream("motor_movement")
    if write_stream is None:
        return ValueError("WriteStream motor_movement not found")

    err = write_stream.Write(
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

    if err is not None:
        logger.error(err)

    return None

    
def on_terminate(sig : signal):
    logger.info("Terminating")
    return None


roverlib.Run(run, on_terminate)
```