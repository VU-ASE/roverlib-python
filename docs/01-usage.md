# Usage

Roverlib comes installed by default on every rover, but if for some reason it isn't, [ssh into the rover](https://ase.vu.nl/docs/tutorials/Fundamental%20Concepts/connecting) and run the following pip install command:

``` bash
pip install roverlib
```

After that, you can use it in a script as shown below, refer to the [service-template-python](https://github.com/VU-ASE/service-template-python) for a complete example.

``` python
#!/usr/bin/python3
import roverlib
import signal
import time
import roverlib.rovercom as rovercom

def run(service : roverlib.Service, configuration : roverlib.ServiceConfiguration):
    
    # Unlike roverlib-go, these functions do not return an error object, but rather throw an error on failure
    speed = configuration.GetFloatSafe("speed")

    name = configuration.GetStringSafe("name")

    write_stream : roverlib.WriteStream = service.GetWriteStream("motor_movement")

    write_stream.Write(
        
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



    
def on_terminate(sig : signal):
    logger.info("Terminating")


roverlib.Run(run, on_terminate)
```
