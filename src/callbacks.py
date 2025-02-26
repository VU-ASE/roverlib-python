"""
d
"""

import signal
from typing import Callable
from configuration import Service, ServiceConfiguration

MainCallBack = Callable[[Service, ServiceConfiguration], Exception]

TerminationCallBack = Callable[[signal.Signals], Exception]
