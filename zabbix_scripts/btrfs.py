#/usr/bin/env python3
"""Description:     Monitor script for BTRFS in Zabbix.
Author:             Olivier van der Toorn <oliviervdtoorn@gmail.com>
"""
import os
import sys
import pdb

SYSFS = '/sys/fs/btrfs'


def get_value(uuid, item):
    """Gets the value for the uuid, item.

    :param uuid: uuid of the filesystem
    :type uuid: str
    :param item: name of item to gather
    :type item: str
    """
    path = os.path.join(
        SYSFS,
        uuid,
        'allocation/data',
        item)
    with open(path, 'r') as fd:
        data = fd.read()

    print(data)

def main():
    """Main function.
    """
    uuid = sys.argv[1]
    item = sys.argv[2]
    get_value(uuid, item)
    pdb.set_trace()


if __name__ == '__main__':
    print(main())
