import pytest
import unittest.mock as mock
from unittest.mock import Mock, patch
from uart import Uart
import time

def counter():
    i = 0
    while True:
        yield i
        i = i + 1

@patch("time.time", side_effect=counter())
@patch("time.sleep")
@patch("uart.serial.Serial")
def test_wait_for_str_ordered_fail(mock_serial, time_sleep, time_time):
    mock_serial.return_value.in_waiting = 0
    mock_serial.return_value.out_waiting = 0
    u = Uart("uart")
    u.log = "baz123\nfoobar123\nbarfoo123\n"
    with pytest.raises(AssertionError) as ex_info:
        u.wait_for_str_ordered(["foo", "bar", "baz"])
    print(ex_info)
    print(ex_info.value)
    u.stop()
    assert "[]" not in str(ex_info.value)

@patch("time.time", side_effect=counter())
@patch("time.sleep")
@patch("uart.serial.Serial")
def test_wait_for_str_ordered(mock_serial, time_sleep, time_time):
    mock_serial.return_value.in_waiting = 0
    mock_serial.return_value.out_waiting = 0
    u = Uart("uart")
    u.log = "\nfoobar123\nbarfoo123\nbaz123\n"
    u.wait_for_str_ordered(["foo", "bar", "baz"])
    u.stop()

@patch("time.time", side_effect=counter())
@patch("time.sleep")
@patch("uart.serial.Serial")
def test_wait_for_str(mock_serial, time_sleep, time_time):
    mock_serial.return_value.in_waiting = 0
    mock_serial.return_value.out_waiting = 0
    u = Uart("uart")
    u.log = "\nfoobar123\nbarfoo123\nbaz123\n"
    u.wait_for_str(["foo", "bar", "baz", "asdf"])
    u.stop()