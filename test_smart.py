#!/usr/bin/env python3
"""Author:      Olivier van der Toorn <oliviervdtoorn@gmail.com>
Description:    Collection of tests for the Zabbix smart script.
"""
import smart


def test_smart_no_arguments():
    """Tests if no arguments gives a zero.
    """
    assert smart.main() == 0


def test_smart_single_argument():
    """Tests if a single argument gives string output (smart output).
    """
    assert isinstance(smart.main('/dev/sda'), str)


def test_smart_two_arguments():
    """Tests the request of a value.
    """
    assert smart.main('/dev/sda', 'Power_On_Hours') != 0
