from ..src.roverlib import init


def test_init():
    r = init()

    print(r.info)
