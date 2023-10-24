"""Unit tests for the 'example' module."""
from teamprojekt_competition_server import example


def test_add():
    # Several test cases for the `add()` function
    assert example.add(0, 0) == 0
    assert example.add(19, 23) == 42
    assert example.add(23, 19) == 42
    assert example.add(1.2, -4.0) == -2.8
