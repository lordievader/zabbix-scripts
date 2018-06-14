#!/usr/bin/python3
import sys
import os
import json
import subprocess

COMMAND = 'udevadm info -a -p /sys/block/{0}|grep usb >/dev/null'
devices = []
FILTER = ['loop']


class BlockDevice():
    def __init__(self, block):
        self.block = block

    def __str__(self):
        return_line = ""
        if self.accept():
            return_line = (
                "{name}\n"
                "\t{disk_type}\n").format(
                    name=self.name,
                    disk_type=self.disk_type)

        return return_line

    def accept(self):
        found = False
        for item in FILTER:
            if item in self.block:
                found = True
                break

        return not found

    @property
    def name(self):
        if self.block.startswith('dm'):
            path = '/sys/block/{0}/dm/name'.format(self.block)
            with open(path, 'r') as name_file:
                name = name_file.read().replace('\n', '')

        else:
            name = self.block

        return name

    @property
    def disk_type(self):
        if 'rimage' in self.name:
            disk_type = 'IMG'

        elif 'rmeta' in self.name:
            disk_type = 'META'

        elif 'dm' in self.block:
            disk_type = 'LVM'

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


def main():
    devices = []
    for block in os.listdir('/sys/block/'):
        device = BlockDevice(block)
        if device.accept() is True:
            devices.append(device.stats)

    data = {'data': devices}
    print(json.dumps(data, sort_keys=True, indent=4))


if __name__ == '__main__':
    main()
