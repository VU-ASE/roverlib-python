import os
import sys
import subprocess
import pickle
import zmq


# Custom types for pre 3.10 support
from typing import Dict, Union

OptionType = Union[int, str, float]

zmq_context = zmq.Context()


# Check whether the python script was launched with roverlib-wrapper
def is_wrapped() -> bool:
    for key in os.environ:
        if "ASE_SW" in key:
            return True
    return False


# Idempotently launches the roverlib-wrapper if not already started.
# This allows the lib to be run standalone, without running roverlib-wrapper.
def attach_wrapper() -> None:
    # If the script was not started with roverlib-wrapper,
    # then launch a subprocess shell with it and halt execution
    # and return same value as subprocess.
    if is_wrapped():
        return

    space_char = " "
    command = f"roverlib-wrapper 'python3 {space_char.join(sys.argv)}'"
    result = subprocess.run(command, shell=True)
    exit(result.returncode)


class Handle:
    def __init__(self, is_subscriber: bool, address: str) -> None:
        self.__is_subscriber = is_subscriber

        if self.__is_subscriber:
            self.__handle = zmq_context.socket(zmq.SUB)
            self.__handle.setsockopt_string(zmq.SUBSCRIBE, "")
            self.__handle.connect(address)
        else:
            self.__handle = zmq_context.socket(zmq.PUB)
            self.__handle.bind(address)

    # Publishes the python object `data` for any subscriber to receive
    def write(self, data: any) -> None:
        if not self.__is_subscriber:
            pickled_bytes = pickle.dumps(data)
            self.__handle.send(pickled_bytes)
        # if any: pickle
        # else: pb.encode

    # Returns python object subscribed to by `name`
    def read(self) -> any:
        if self.__is_subscriber:
            pickled_bytes = self.__handle.recv()
            return pickle.loads(pickled_bytes)


class Rover:
    def __init__(self) -> None:
        attach_wrapper()

        self.info = {}
        self.pid: int = 0
        self.name: str = ""
        
        # Each zmq socket is identified with its name
        self.__subs: Dict[str, Handle] = {}
        self.__pubs: Dict[str, Handle] = {}

        self.options: Dict[str, OptionType] = {}

        option_set = set()

        for key, value in os.environ.items():
            if "ASE" in key:
                self.info[key] = value

                if "ServicePID" in key:
                    self.pid = int(value)
                elif "ServiceName" in key:
                    self.name = str(value)
                elif "TuningParameter" in key:
                    option_name = key.split("ASE_SW_TuningParameter")[1].split("_")[1]
                    option_set.add(option_name)
                elif "Output" in key:
                    name = key.split("ASE_SW_Output_")[1]
                    self.__pubs[name] = Handle(False, value)
                elif "Dependency" in key and "core_broadcast" not in key:
                    name = key.split("ASE_SW_Dependency_")[1]
                    self.__subs[name] = Handle(True, value)

        for option_name in option_set:
            if os.environ[f"ASE_SW_TuningParameterType_{option_name}"] == "Int":
                self.options[option_name] = int(
                    os.environ[f"ASE_SW_TuningParameterValue_{option_name}"]
                )
            elif os.environ[f"ASE_SW_TuningParameterType_{option_name}"] == "Float":
                self.options[option_name] = float(
                    os.environ[f"ASE_SW_TuningParameterValue_{option_name}"]
                )
            elif os.environ[f"ASE_SW_TuningParameterType_{option_name}"] == "String":
                self.options[option_name] = str(
                    os.environ[f"ASE_SW_TuningParameterValue_{option_name}"]
                )

    def publish(self, name: str) -> Handle:
        return self.__pubs[name]

    def subscribe(self, service_name: str, stream_name: str) -> Handle:
        return self.__subs[f"{service_name}_{stream_name}"]

    def print_info(self) -> None:
        if self.info:
            print(f">>> Name: {self.name}")
            print(f">>> PID: {self.pid}")
            print(f">>> Number of subscription handles: {len(self.__subs)}")
            print(f">>> Number of publish handles: {len(self.__pubs)}")

            print(">>> Options:")
            if len(self.options) == 0:
                print("    {}")
            for key, value in self.options.items():
                print(f"    {key}: {value} {type(value)}")

            print(">>> Env:")
            for key, value in self.info.items():
                print(f"    {key}: {value}")

            sys.stdout.flush()

    def log(self, m: any = "") -> None:
        print(m)
        sys.stdout.flush()


def init() -> Rover:
    return Rover()
