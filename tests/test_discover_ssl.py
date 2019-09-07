#!/usr/bin/env python3
"""Author:      Olivier van der Toorn <oliviervdtoorn@gmail.com>
Description:    Collection of tests for the Zabbix discovery scripts.
"""
import json
import os
import pdb
from unittest import mock
from io import StringIO
from pytest_mock import mocker as _mocker  # noqa: F401

from zabbix_scripts import discover_ssl


def test_discover_ssl(mocker):
    """Checks if discover_ssl returns valid json.
    """
    assert json.JSONDecoder().decode(discover_ssl.main()) == {'data': []}

    output = {
        'data': [
            {
                '{#URL}': 'example.org',
                '{#PORT}': '443',
            },
            {
                '{#URL}': 'example.org',
                '{#PORT}': '8080',
            },
        ]
    }
    with open('tests/urls.txt', 'r') as urls:
        with mocker.patch.object(discover_ssl, 'open', return_value=urls):
            assert json.JSONDecoder().decode(discover_ssl.main()) == output
