#!/usr/bin/env python3
"""Author:      Olivier van der Toorn <oliviervdtoorn@gmail.com>
Description:    Collection of tests for the Zabbix discovery scripts.
"""
import json
from unittest import mock
from io import StringIO
from pytest_mock import mocker as _mocker  # noqa: F401

from zabbix_scripts import discover_iostat


def test_blockdevices(mocker):
    """Tests the blockdevices function.
    """
    with open('tests/iostat-N', 'r') as iostat_N:
        output = iostat_N.read()
    with mocker.patch.object(discover_iostat.subprocess, 'getoutput',
                             return_value=output):
        assert discover_iostat.blockdevices() == [
            {'{#BLOCK}': 'sda'},
            {'{#BLOCK}': 'ssd'},
        ]


def test_discover_iostat():
    """Checks if discover_iostat returns valid json.
    """
    json.JSONDecoder().decode(discover_iostat.main())
