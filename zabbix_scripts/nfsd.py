#!/usr/bin/env python3
"""Author:      Olivier van der Toorn <oliviervdtoorn@gmail.com>
Description:    Parser for /proc/net/rpc/nfsd
Based on: https://www.svennd.be/nfsd-stats-explained-procnetrpcnfsd/
"""
import pdb
import pprint
import json
import os
import collections

NFSD_FILE = '/proc/net/rpc/nfsd'
KEYS = {
    'rc': ('Reply Cache', ('hits', 'misses', 'nocache')),
    'fh': ('File Handles', ('stale', 'total_lookups', 'anonlookups',
           'dirnocache', 'nodirnocache')),
    'io': ('IO', ('read', 'write')),
    'th': ('Threads', ('threads', 'fullcnt', 'deprecated_histogram')),
    'ra': ('Read Ahead Cache', ('cachesize', '10%', '20%', '30%', '40%', '50%',
           '60%', '70%', '80%', '90%', '100%', 'notfound')),
    'net': ('Network', ('netcount', 'udpcount', 'tcpcount', 'tcpconnect')),
    'rpc': ('RPC', ('count', 'badcnt', 'badfmt', 'badauth', 'badcInt')),
    'proc3': ('Proc3', ('values_to_follow', 'null', 'getattr', 'setattr',
                        'lookup', 'access', 'readlink', 'read', 'write',
                        'create', 'mkdir', 'symlink', 'mknod', 'remove',
                        'rmdir', 'rename', 'link', 'readdir', 'readdirplus',
                        'fsstat', 'fsinfo', 'pathconf', 'commit')),
    'proc4': ('Proc4', ('values_to_follow', 'null', 'compound')),
}
NFS4_KEYS = [
    'op0-unused',
    'op1-unused',
    'op2-future',
    'access',
    'close',
    'commit',
    'create',
    'delegpurge',
    'delegreturn',
    'getattr',
    'getfh',
    'link',
    'lock',
    'lockt',
    'locku',
    'lookup',
    'lookupp',
    'nverify',
    'open',
    'openattr',
    'open_confirm',
    'open_dgrd',
    'putfh',
    'putpubfh',
    'putrootfh',
    'read',
    'readdir',
    'readlink',
    'remove',
    'rename',
    'renew',
    'restorefh',
    'savefh',
    'secinfo',
    'setattr',
    'setcltid',
    'setcltidconf',
    'verify',
    'write',
    'rellockowner',
]


def nfsd_exists():
    """Tests if /proc/net/rpc/nfsd exists.
    """
    return os.path.isfile(NFSD_FILE)


def parse(nfsd):
    """Parses the nfsd file into a (named) dictionary.

    :param nfsd: raw input from /proc/net/rpc/nfsd
    :type nfsd: str
    :return: dictionary
    """
    parsed = {}
    for line in nfsd.split('\n'):
        values = collections.deque(line.split(' '))
        key = values.popleft()
        if key in KEYS:
            name, items = KEYS[key]
            parsed[name] = dict(zip(items, values))

        elif key == 'proc4ops':
            parsed['Proc4ops'] = dict(zip(
                NFS4_KEYS, list(values)[0:len(NFS4_KEYS)]))

    return parsed


def to_json(nfsd):
    """Converts the output of `parse` to JSON for Zabbix.

    :param nfsd: the output of `parse`
    :type nfsd: dict
    """
    return json.dumps(nfsd, sort_keys=True, indent=4)


def main():
    """Main function.
    """
    parsed = {}
    if nfsd_exists() is True:
        with open(NFSD_FILE, 'r') as nfsd_file:
            nfsd_input = nfsd_file.read()

        parsed = parse(nfsd_input)

    return to_json(parsed)


if __name__ == '__main__':
    print(main())  # pragma: no cover
