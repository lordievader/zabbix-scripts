#!/usr/bin/env python3
"""Description: Discovers for block devices for Zabbix.
Author: Olivier van der Toorn.
"""
import os
import json
import sys


DEVICES = []
FILTER = ['loop', 'meta']


class BlockDevice():
    """Abstraction of a block device.
    """

    def __init__(self, block):
        """Init fuction of block device.

        :param block: name of block
        :type block: str
        :return: None
        """
        self.block = block

    @property
    def name(self):
        """Gives the block device a name.

        :return: name of block device
        """
        if self.block.startswith('dm'):
            path = '/sys/block/{0}/dm/name'.format(self.block)
            with open(path, 'r') as name_file:
                name = name_file.read().replace('\n', '')

        else:
            name = self.block

        return name

    @property
    def size(self):
        """Returns the size of the block device.

        :return: int size of disk
        """
        path = '/sys/block/{0}/size'.format(self.block)
        with open(path, 'r') as size_file:
            size = int(size_file.read().replace('/n', ''))

        return size

    @property
    def disk_type(self):
        """Returns the disk type. These are in no way 'official', my definition
        of types of block devices.

        :return: str of block device
        """
        if 'rimage' in self.name:
            disk_type = 'IMG'

        elif 'rmeta' in self.name:
            disk_type = 'META'

        elif 'dm' in self.block:
            disk_type = 'LVM'

        elif 'md' in self.block:
            disk_type = 'MD'

        else:
            path = '/sys/block/{0}/queue/rotational'.format(self.block)
            with open(path, 'r') as rotational:
                if rotational.read().replace('\n', '') == '1':
                    disk_type = 'HDD'

                else:
                    disk_type = 'SSD'

        return disk_type

    @property
    def stats(self):
        stats = {
            '{#DISKNAME}': os.path.join('/dev/', self.block),
            '{#SHORTDISKNAME}': self.name,
            '{#DISKTYPE}': self.disk_type,
        }
        return stats

    def accept(self):
        """Should this block device be discovered?

        :return: boolean
        """
        found = False
        if self.size == 0:
            return found

        for item in FILTER:
            if item in self.block:
                found = True
                break

        return not found


def main():
    """Main discovery function.
    """
    args = sys.argv
    if len(args) == 1:
        disk_type = 'ALL'

    elif len(args) > 1:
        disk_type = args[1].upper()

    devices = []
    for block in os.listdir('/sys/block/'):
        device = BlockDevice(block)
        if (device.accept() is True and (
                disk_type == 'ALL' or device.disk_type == disk_type)):
            devices.append(device.stats)

    data = {'data': devices}
    return json.dumps(data, sort_keys=True, indent=4)


if __name__ == '__main__':
    print(main())  # pragma: no cover
