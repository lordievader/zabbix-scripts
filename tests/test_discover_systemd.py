#!/usr/bin/env python3
"""Author:      Olivier van der Toorn <oliviervdtoorn@gmail.com>
Description:    Collection of tests for the Zabbix discovery scripts.
"""
import json
import subprocess
from unittest import mock
from pytest_mock import mocker as _mocker  # noqa: F401

from zabbix_scripts import discover_systemd


def raisecalledprocesserror(*args, **kwargs):
    """Raises a subprocess.CalledProcessError
    """
    raise subprocess.CalledProcessError(1, 'mocked process')


def test_discover_systemd(mocker):
    """Checks if discover_systemd returns valid json.
    """
    with mocker.patch.object(
            discover_systemd.subprocess, 'run',
            side_effect=raisecalledprocesserror):
        test_output = json.JSONDecoder().decode(discover_systemd.main())
        assert test_output == {'data': []}

    with open('tests/systemd', 'rb') as systemd:
        output = systemd.read()

    with mock.patch(
            'zabbix_scripts.discover_systemd.subprocess.run',
            new_callable=mock.MagicMock) as mock_pvs:
        type(mock_pvs.return_value).stdout = mock.PropertyMock(
            return_value=output)
        test_output = json.JSONDecoder().decode(discover_systemd.main())

        assert test_output == {
            'data': [
                {
                    '{#NAME}': 'bluetooth.service',
                    '{#SERVICENAME}': 'bluetooth.service',
                },
                {
                    '{#NAME}': 'dbus.service',
                    '{#SERVICENAME}': 'dbus.service',
                },
            ]
        }
