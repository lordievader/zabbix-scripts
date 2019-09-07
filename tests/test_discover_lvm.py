#!/usr/bin/env python3
"""Author:      Olivier van der Toorn <oliviervdtoorn@gmail.com>
Description:    Collection of tests for the Zabbix discovery scripts.
"""
import json
import subprocess
from unittest import mock
from pytest_mock import mocker as _mocker  # noqa: F401

from zabbix_scripts import discover_lvm


def raisecalledprocesserror(*args, **kwargs):
    """Raises a subprocess.CalledProcessError
    """
    raise subprocess.CalledProcessError(1, 'mocked process')


def test_check_lvm(mocker):
    """Tests the check_lvm function.
    """
    with mocker.patch.object(discover_lvm.subprocess, 'check_call'):
        assert discover_lvm.check_lvm() is True

    with mocker.patch.object(
            discover_lvm.subprocess, 'check_call',
            side_effect=raisecalledprocesserror):
        assert discover_lvm.check_lvm() is False


def test_physical_volumes(mocker):
    """Tests the physical_volumes function.
    """
    with open('tests/pvs', 'rb') as pvs:
        output = pvs.read()

    with mocker.patch.object(
            discover_lvm, 'check_lvm', return_value=True):
        with mock.patch(
                'zabbix_scripts.discover_lvm.subprocess.run',
                new_callable=mock.MagicMock) as mock_pvs:
            type(mock_pvs.return_value).stdout = mock.PropertyMock(
                return_value=output)
            assert discover_lvm.physical_volumes() == [
                {
                    '{#SHORTNAME}': 'ssd',
                    '{#VOLUME}': '/dev/mapper/ssd',
                },
            ]


def test_volume_groups(mocker):
    """Tests the physical_volumes function.
    """
    with open('tests/vgs', 'rb') as vgs:
        output = vgs.read()

    with mocker.patch.object(
            discover_lvm, 'check_lvm', return_value=True):
        with mock.patch(
                'zabbix_scripts.discover_lvm.subprocess.run',
                new_callable=mock.MagicMock) as mock_pvs:
            type(mock_pvs.return_value).stdout = mock.PropertyMock(
                return_value=output)
            assert discover_lvm.volume_groups() == [
                {
                    '{#SHORTNAME}': 'scimitar-vg',
                },
            ]


def test_logical_volume(mocker):
    """Tests the physical_volumes function.
    """
    with open('tests/lvs', 'rb') as lvs:
        output = lvs.read()

    with mocker.patch.object(
            discover_lvm, 'check_lvm', return_value=True):
        with mock.patch(
                'zabbix_scripts.discover_lvm.subprocess.run',
                new_callable=mock.MagicMock) as mock_pvs:
            type(mock_pvs.return_value).stdout = mock.PropertyMock(
                return_value=output)
            assert discover_lvm.logical_volumes() == [
                {
                    '{#SHORTNAME}': 'home-lv',
                    '{#VOLUME}': '/dev/scimitar-vg/home-lv',
                },
                {
                    '{#SHORTNAME}': 'thinpool-lv',
                    '{#VOLUME}': 'thinpool-lv',
                },
            ]


def test_discover_lvm(mocker):
    """Checks if discover_lvm returns valid json.
    """
    pvs = {
        '{#SHORTNAME}': 'ssd',
        '{#VOLUME}': '/dev/mapper/ssd',
    }
    vgs = {
        '{#SHORTNAME}': 'scimitar-vg',
    }
    lvs = [
        {
            '{#SHORTNAME}': 'home-lv',
            '{#VOLUME}': '/dev/scimitar-vg/home-lv',
        },
        {
            '{#SHORTNAME}': 'thinpool-lv',
            '{#VOLUME}': 'thinpool-lv',
        },
    ]

    with mocker.patch.object(discover_lvm, 'physical_volumes',
                             return_value=pvs):
        output = json.JSONDecoder().decode(discover_lvm.main('pv'))
        assert output == {'data': pvs}

    with mocker.patch.object(discover_lvm, 'volume_groups',
                             return_value=vgs):
        output = json.JSONDecoder().decode(discover_lvm.main('vg'))
        assert output == {'data': vgs}

    with mocker.patch.object(discover_lvm, 'logical_volumes',
                             return_value=lvs):
        output = json.JSONDecoder().decode(discover_lvm.main('lv'))
        assert output == {'data': lvs}

    assert json.JSONDecoder().decode(discover_lvm.main()) == {'data': []}
