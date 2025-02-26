import signal
from typing import Callable
from configuration import Service, ServiceConfiguration

MainCallback = Callable[[Service, ServiceConfiguration], Exception]

TerminationCallback = Callable[[signal.Signals], Exception]
