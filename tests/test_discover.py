#!/usr/bin/env python3
"""Author:      Olivier van der Toorn <oliviervdtoorn@gmail.com>
Description:    Collection of tests for the Zabbix discovery scripts.
"""
import json

from zabbix_scripts import discover_block
from zabbix_scripts import discover_clustermanager
from zabbix_scripts import discover_files
from zabbix_scripts import discover_iostat
from zabbix_scripts import discover_lvm
from zabbix_scripts import discover_ports
from zabbix_scripts import discover_sensors
from zabbix_scripts import discover_ssl
from zabbix_scripts import discover_systemd


def test_discover_block():
    """Checks if discover_block returns valid json.
    """
    json.JSONDecoder().decode(discover_block.main())


def test_discover_clustermanager():
    """Checks if discover_clustermanager returns valid json.
    """
    json.JSONDecoder().decode(discover_clustermanager.main())


def test_discover_files():
    """Checks if discover_files returns valid json.
    """
    json.JSONDecoder().decode(discover_files.main())


def test_discover_iostat():
    """Checks if discover_iostat returns valid json.
    """
    json.JSONDecoder().decode(discover_iostat.main())


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


def test_discover_systemd():
    """Checks if discover_systemd returns valid json.
    """
    json.JSONDecoder().decode(discover_systemd.main())
