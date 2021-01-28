#/usr/bin/env python3
"""Description:     Monitor script for BTRFS in Zabbix.
Author:             Olivier van der Toorn <oliviervdtoorn@gmail.com>
"""
import os
import sys

SYSFS = '/sys/fs/btrfs'


def check():
    """Checks if the SYSFS folder exists.
    """
    return os.path.isdir(SYSFS)


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
        'allocation',
        item)
    with open(path, 'r') as file_descriptor:
        data = file_descriptor.read()

    return data.replace('\n', '')


def main():
    """Main function. The function/script uses
    sysv arguments to find the BTRFS filesystem
    and what data is requested.

    argv0: uuid of the btrfs (as in /sys/fs/btrfs)
    argv1: data requests, can be anything from
    /sys/fs/btrfs/<uuid>/allocation

    For example argv1 can be 'data/bytes_used'.
    """
    output = 0
    if check():
        uuid = sys.argv[1]
        item = sys.argv[2]
        output = get_value(uuid, item)

    return output


if __name__ == '__main__':
    print(main())
