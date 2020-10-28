#!/usr/bin/env python3
"""Author:          Olivier van der Toorn <olivier@snt.utwente.nl>
Description:        Discover script for BTRFS filesystems.
"""
import os
import json
import pdb


def uuids(basedir='/sys/fs/btrfs'):
    """Gathers the UUIDs from the basedir.
    The basedir defaults to `/sys/fs/btrfs`.

    :param basedir: directory to scan for UUIDs
    :type basedir: str
    :return: list of paths
    """
    uuid = os.listdir(basedir)
    uuid.remove('features')
    uuid = {item: os.path.join(basedir, item) for item in uuid}
    return uuid

def disk_names(uuids):
    """Translates UUIDs to device names (dm-N, sdXY).

    :param uuids: list of uuids
    :type uuids: list
    :return: dict of uuid: device name
    """
    path = '/dev/disk/by-uuid'
    names = {}
    for uuid in uuids:
        dst = os.readlink(os.path.join(path, uuid))
        name = os.path.split(dst)[1]
        names[uuid] = name

    return names


def main():
    """Main function, calls all the other functions.
    """
    uuid = uuids()
    names = disk_names(list(uuid.keys()))
    btrfs = []
    for key, value in uuid.items():
        name = names[key]
        btrfs.append(
            {
                '{#SHORTNAME}': name,
                '{#PATH}': value,
            }
        )

    return json.dumps(btrfs, sort_keys=True, indent=4)


if __name__ == '__main__':
    print(main())
