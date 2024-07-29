class Rover:
    def __init__(self, custom_name: str) -> None:
        self.info = {}
        self.info["name"] = custom_name


def init(name: str) -> bool:
    if not name:
        return Rover(custom_name="Python Rover")
    else:
        return Rover(name)
