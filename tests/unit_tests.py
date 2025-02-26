"""
General unit tests.
"""

import roverlib as rover

def test_greet():
    assert rover.greet("Test") == "Hello, Test!"

def test_bye():
    assert rover.bye() == "Goodbye!"

