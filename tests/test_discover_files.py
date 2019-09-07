#!/usr/bin/env python3
"""Author:      Olivier van der Toorn <oliviervdtoorn@gmail.com>
Description:    Collection of tests for the Zabbix discovery scripts.
"""
import json
from unittest import mock
from io import StringIO
from pytest_mock import mocker as _mocker  # noqa: F401

from zabbix_scripts import discover_files


def test_discover_files():
    """Checks if discover_files returns valid json.
    """
    with mock.patch('sys.argv', ['./discover_block.py']):
        json.JSONDecoder().decode(discover_files.main())

    with mock.patch('sys.argv', ['./discover_block.py', 'notadir']):
        assert json.JSONDecoder().decode(discover_files.main()) == {'data': []}
