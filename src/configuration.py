import threading
import time
from loguru import logger
from bootinfo import Service, TypeEnum


class ServiceConfiguration:
    def __init__(self):
        self.floatOptions : dict[str, float] = {}
        self.stringOptions : dict[str, str] = {}
        self.tunable : dict[str, bool] = {}
        self.lock = threading.RLock()
        self.lastUpdate : int = int(time.time() * 1000)
    
    # Returns the float value of the configuration option with the given name, returns an error if the option does not exist or does not exist for this type
    # Reading is NOT thread-safe, but we accept the risks because we assume that the user program will read the configuration values repeatedly
    # If you want to read the configuration values concurrently, you should use the GetFloatSafe method
    def GetFloat(self, name : str):
        logger.debug(self.floatOptions)
        if name not in self.floatOptions:
            return None, "No float configuration option with name %s" % name
        
        return self.floatOptions[name], None
        
    def GetFloatSafe(self, name : str):
        with self.lock:
            return self.GetFloat(name)


    # Returns the string value of the configuration option with the given name, returns an error if the option does not exist or does not exist for this type
    # Reading is NOT thread-safe, but we accept the risks because we assume that the user program will read the configuration values repeatedly
    # If you want to read the configuration values concurrently, you should use the GetStringSafe method    
    def GetString(self, name : str):
        if name not in self.stringOptions:
            return None, "No string configuration option with name %s" % name
        
        return self.stringOptions[name], None
        
    def GetStringSafe(self, name : str):
        with self.lock:
            return self.GetString(name)

    # Set the float value of the configuration option with the given name (thread-safe)    
    def _setFloat(self, name : str, value : float):
        with self.lock:
            if name in self.tunable:
                if name not in self.floatOptions:
                    logger.error("%s : %s Is not of type Float" % (name, value))
                self.floatOptions[name] = value
                logger.info("%s : %f Set float configuration option" % (name, value))
            else:
                logger.error("%s : %f Attempted to set non-tunable float configuration option" % (name, value))
    
    # Set the string value of the configuration option with the given name (thread-safe)
    def _setString(self, name : str, value : str):
        with self.lock:
            if name in self.tunable:
                if name not in self.stringOptions:
                    logger.error("%s : %f Is not of type String" % (name, value))
                    return None
                self.floatOptions[name] = value
                logger.info("%s : %s Set string configuration option" % (name, value))
            else:
                logger.error("%s : %s Attempted to set non-tunable string configuration option" % (name, value))



def NewServiceConfiguration(service : Service):
    config = ServiceConfiguration()
    for c in service.configuration:

        if c.type == TypeEnum.NUMBER:
            config.floatOptions[c.name] = c.value
        elif c.type == TypeEnum.STRING:
            config.stringOptions[c.name] = c.value
        
        if c.tunable is True:
            config.tunable[c.name] = c.tunable

    return config

