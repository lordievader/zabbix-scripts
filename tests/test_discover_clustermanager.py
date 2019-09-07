#!/usr/bin/env python3
"""Author:      Olivier van der Toorn <oliviervdtoorn@gmail.com>
Description:    Collection of tests for the Zabbix discovery scripts.
"""
import json
from pytest_mock import mocker as _mocker  # noqa: F401

from zabbix_scripts import discover_clustermanager


def raisefilenotfounderror(*args, **kwargs):  # pylint: disable=unused-argument
    """Raises a FileNotFoundError.
    """
    raise FileNotFoundError('mocked')


def test_discover_clustermanager(mocker):
    """Checks if discover_clustermanager returns valid json.
    """
    with mocker.patch.object(discover_clustermanager, 'open',
                             side_effect=raisefilenotfounderror):
        output = json.JSONDecoder().decode(discover_clustermanager.main())
        assert output == {'data': []}

    with mocker.patch.object(discover_clustermanager, 'open',
                             return_value=open('tests/clustermanager', 'r')):
        output = json.JSONDecoder().decode(discover_clustermanager.main())
        assert output == {
            'data': [
                {
                    '{#CMNAME}': 'Infra NS',
                    '{#CMINDEX}': '1'
                },
                {
                    '{#CMNAME}': 'Infra TLSA port 25',
                    '{#CMINDEX}': '3'
                },
                {
                    '{#CMNAME}': 'RBL',
                    '{#CMINDEX}': '6'
                },
            ]
        }
