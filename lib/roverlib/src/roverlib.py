import os


class Rover:
    def __init__(self) -> None:
        self.info = {}

        while True:
            for key, value in os.environ.items():
                if "ASE" in key:
                    self.info[key] = value


def init() -> Rover:
    return Rover()
