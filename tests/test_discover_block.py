#!/usr/bin/env python3
"""Author:      Olivier van der Toorn <oliviervdtoorn@gmail.com>
Description:    Collection of tests for the Zabbix discovery scripts.
"""
import json
from unittest import mock
from io import StringIO
from pytest_mock import mocker as _mocker  # noqa: F401

from zabbix_scripts import discover_block


def test_blockdevice():
    """Tests the init fuction of BlockDevice.
    """
    block = discover_block.BlockDevice('test')
    assert block.block == 'test'


def test_name(mocker):
    """Tests the size property of the BlockDevice.
    """
    block = discover_block.BlockDevice('dmtest')
    with mocker.patch.object(discover_block, 'open',
                             return_value=StringIO('testing')):
        assert block.name == 'testing'

    del block
    block = discover_block.BlockDevice('test')
    assert block.name == 'test'


def test_size(mocker):
    """Tests the size attribute of the BlockDevice.
    """
    block = discover_block.BlockDevice('test')
    with mocker.patch.object(discover_block, 'open',
                             return_value=StringIO('10\n')):
        assert block.size == 10


def test_type(mocker):
    """Tests the size attribute of the BlockDevice.
    """
    assert discover_block.BlockDevice('rimage-test').disk_type == 'IMG'
    assert discover_block.BlockDevice('rmeta-test').disk_type == 'META'
    assert discover_block.BlockDevice('mdtest').disk_type == 'MD'

    with mocker.patch.object(discover_block, 'open',
                             return_value=StringIO('dmtest')):
        with mocker.patch.object(discover_block.BlockDevice, 'name',
                                 return_value='dmtest'):
            assert discover_block.BlockDevice('dmtest').disk_type == 'LVM'

    hdd = discover_block.BlockDevice('test')
    with mocker.patch.object(discover_block, 'open',
                             return_value=StringIO('1\n')):
        assert hdd.disk_type == 'HDD'

    ssd = discover_block.BlockDevice('test')
    with mocker.patch.object(discover_block, 'open',
                             return_value=StringIO('0\n')):
        assert ssd.disk_type == 'SSD'


def test_stats(mocker):
    """Tests the stats attribute of the BlockDevice.
    """
    assert discover_block.BlockDevice('mdtest').stats == {
        '{#DISKNAME}': '/dev/mdtest',
        '{#SHORTDISKNAME}': 'mdtest',
        '{#DISKTYPE}': 'MD'
    }


def test_accept(mocker):
    """Tests the accept function.
    """
    with mock.patch(
            'zabbix_scripts.discover_block.BlockDevice.size',
            new_callable=mock.PropertyMock) as mock_size:
        mock_size.return_value = 0
        assert discover_block.BlockDevice('test').accept() is False

        mock_size.return_value = 1
        assert discover_block.BlockDevice('test').accept() is True
        assert discover_block.BlockDevice('loop0').accept() is False
        assert discover_block.BlockDevice('meta0').accept() is False


def test_discover_block():
    """Checks if discover_block returns valid json.
    """
    with mock.patch('sys.argv', ['./discover_block.py']):
        json.JSONDecoder().decode(discover_block.main())

    with mock.patch('sys.argv', ['./discover_block.py', 'lvm']):
        json.JSONDecoder().decode(discover_block.main())
