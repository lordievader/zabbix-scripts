#!/usr/bin/env python3
"""Author:      Olivier van der Toorn <oliviervdtoorn@gmail.com>
Description:    Collection of tests for the Zabbix discovery scripts.
"""
import json

import discover_block
import discover_lvm
import discover_ports
import discover_sensors
import discover_ssl


def test_discover_block():
    """Checks if discover_block returns valid json.
    """
    json.JSONDecoder().decode(discover_block.main())


def test_discover_lvm():
    """Checks if discover_lvm returns valid json.
    """
    json.JSONDecoder().decode(discover_lvm.main())


def test_discover_ports():
    """Checks if discover_ports returns valid json.
    """
    json.JSONDecoder().decode(discover_ports.main())


def test_discover_sensors():
    """Checks if discover_sensors returns valid json.
    """
    json.JSONDecoder().decode(discover_sensors.main())


def test_discover_ssl():
    """Checks if discover_ssl returns valid json.
    """
    json.JSONDecoder().decode(discover_ssl.main())
