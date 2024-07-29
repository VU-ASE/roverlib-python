from ..src.roverlib import init


def test_init():
    r = init("My Rover")

    assert r.info["name"] == "My Rover"
