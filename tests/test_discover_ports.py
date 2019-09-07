#!/usr/bin/env python3
"""Author:      Olivier van der Toorn <oliviervdtoorn@gmail.com>
Description:    Collection of tests for the Zabbix discovery scripts.
"""
import json
from pytest_mock import mocker as _mocker  # noqa: F401

from zabbix_scripts import discover_ports


def test_discover_ports(mocker):
    """Checks if discover_ports returns valid json.
    """
    assert json.JSONDecoder().decode(discover_ports.main()) == {'data': []}

    output = {
        'data': [
            {
                '{#IP}': '127.0.0.1',
                '{#PORT}': '22',
                '{#METHOD}': 'tcp',
            },
            {
                '{#IP}': '127.0.0.1',
                '{#PORT}': '22',
                '{#METHOD}': 'ssh',
            },
            {
                '{#IP}': '127.0.0.1',
                '{#PORT}': '2222',
                '{#METHOD}': 'tcp',
            },
            {
                '{#IP}': '127.0.0.1',
                '{#PORT}': '2222',
                '{#METHOD}': 'ssh',
            },
            {
                '{#IP}': 'example.org',
                '{#PORT}': '2020',
                '{#METHOD}': 'tcp',
            },
            {
                '{#IP}': 'example.org',
                '{#PORT}': '2020',
                '{#METHOD}': 'ssh',
            },
        ]
    }
    with open('tests/ports.txt', 'r') as ports:
        with mocker.patch.object(discover_ports, 'open', return_value=ports):
            assert json.JSONDecoder().decode(discover_ports.main()) == output
