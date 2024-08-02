import os
import sys
import subprocess

# Custom types for pre 3.10 support
from typing import Dict, Union

OptionType = Union[int, str, float]


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


class Rover:
    def __init__(self) -> None:
        attach_wrapper()

        self.info = {}
        self.pid: int = 0
        self.name: str = ""
        self.input_handles: Dict[str, any] = {}
        self.output_handles: Dict[str, any] = {}
        self.options: Dict[str, OptionType] = {}

        option_set = set()

        import zmq

        zmq_context = zmq.Context()

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
                    self.output_handles[name] = zmq_context.socket(zmq.REP)
                    self.output_handles[name].bind(value)
                elif "Dependency" in key and "core_broadcast" not in key:
                    name = key.split("ASE_SW_Dependency_")[1]
                    self.input_handles[name] = zmq_context.socket(zmq.REQ)
                    self.input_handles[name].connect(value)

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

    def print_info(self) -> None:
        if self.info:
            print("--- Env ---")
            for key, value in self.info.items():
                print(f"{key}: {value}")

            print("--- Options ---")
            for key, value in self.options.items():
                print(f"{key}: {value} {type(value)}")

            print("--- in handles ---")
            for key, value in self.input_handles.items():
                print(f"{key}: {value} {type(value)}")

            print("--- out handles ---")
            for key, value in self.output_handles.items():
                print(f"{key}: {value} {type(value)}")

            sys.stdout.flush()


def init() -> Rover:
    return Rover()
