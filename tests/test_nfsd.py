#!/usr/bin/env python3
"""Author:      Olivier van der Toorn <oliviervdtoorn@gmail.com>
Description:    Tests for the /proc/net/rpc/nfsd
"""
import json
from zabbix_scripts import nfsd

PARSED = {
    'File Handles': {'anonlookups': '0',
                     'dirnocache': '0',
                     'nodirnocache': '0',
                     'stale': '70',
                     'total_lookups': '0'},
    'IO': {'read': '805423065', 'write': '3188835811'},
    'Network': {'netcount': '2196079',
                'tcpconnect': '318',
                'tcpcount': '2196854',
                'udpcount': '0'},
    'Proc3': {'access': '4',
              'commit': '0',
              'create': '0',
              'fsinfo': '8',
              'fsstat': '139',
              'getattr': '368',
              'link': '0',
              'lookup': '3',
              'mkdir': '0',
              'mknod': '0',
              'null': '6',
              'pathconf': '4',
              'read': '0',
              'readdir': '0',
              'readdirplus': '42',
              'readlink': '0',
              'remove': '0',
              'rename': '0',
              'rmdir': '0',
              'setattr': '0',
              'symlink': '0',
              'values_to_follow': '22',
              'write': '0'},
    'Proc4': {'compound': '2195384', 'null': '57', 'values_to_follow': '2'},
    'Proc4ops': {'access': '0',
                 'close': '215047',
                 'commit': '76075',
                 'create': '1467',
                 'delegpurge': '147',
                 'delegreturn': '0',
                 'getattr': '70015',
                 'getfh': '1152653',
                 'link': '100508',
                 'lock': '98',
                 'lockt': '3',
                 'locku': '0',
                 'lookup': '3',
                 'lookupp': '92246',
                 'nverify': '0',
                 'op0-unused': '72',
                 'op1-unused': '0',
                 'op2-future': '0',
                 'open': '0',
                 'open_confirm': '0',
                 'open_dgrd': '233',
                 'openattr': '84486',
                 'putfh': '6',
                 'putpubfh': '1385263',
                 'putrootfh': '0',
                 'read': '348',
                 'readdir': '86794',
                 'readlink': '62150',
                 'rellockowner': '56068',
                 'remove': '41',
                 'rename': '1546',
                 'renew': '3912',
                 'restorefh': '6862',
                 'savefh': '98',
                 'secinfo': '4010',
                 'setattr': '0',
                 'setcltid': '17945',
                 'setcltidconf': '45',
                 'verify': '45',
                 'write': '0'},
    'RPC': {'badauth': '12',
            'badcInt': '0',
            'badcnt': '16',
            'badfmt': '4',
            'count': '2196034'},
    'Read Ahead Cache': {'10%': '0',
                         '20%': '0',
                         '30%': '0',
                         '40%': '0',
                         '50%': '0',
                         '60%': '0',
                         '70%': '0',
                         '80%': '0',
                         '90%': '0',
                         '100%': '0',
                         'cachesize': '32',
                         'notfound': '0'},
    'Reply Cache': {'hits': '0', 'misses': '8274', 'nocache': '2187711'},
    'Threads': {
        'deprecated_histogram': '0.000', 'fullcnt': '0', 'threads': '8'
    }
}


def test_find_file(mocker):
    """Test the finding of the nfsd file.
    """
    with mocker.patch.object(nfsd.os.path, 'isfile', return_value=True):
        assert nfsd.nfsd_exists() is True

    with mocker.patch.object(nfsd.os.path, 'isfile', return_value=False):
        assert nfsd.nfsd_exists() is False


def test_parser(mocker):
    """Tests the parsing of an example input.
    """
    with open('tests/nfsd.txt', 'r') as test_file:
        nfsd_input = test_file.read()

    assert nfsd.parse(nfsd_input) == PARSED


def test_to_json():
    """Tests if the correct json is outputted.
    """
    assert json.JSONDecoder().decode(nfsd.to_json(PARSED)) == PARSED


def test_main(mocker):
    """Tests the main function of nfsd.
    """
    with open('tests/nfsd.txt', 'r') as test_file:
        with mocker.patch.object(nfsd, 'nfsd_exists', return_value=True):
            with mocker.patch.object(nfsd, 'open', return_value=test_file):
                assert json.JSONDecoder().decode(nfsd.main()) == PARSED

    with mocker.patch.object(nfsd, 'nfsd_exists', return_value=False):
        assert json.JSONDecoder().decode(nfsd.main()) == {}
