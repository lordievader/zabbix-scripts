#!/usr/bin/env python3
""" Description: Discovers lvm related things.
Author:          Olivier van der Toorn <oliviervdtoorn@gmail.com>"""
import json
import re
import subprocess
import sys


def physical_volumes():
    """Returns the discovered physical volumes.
    """
    command = ['sudo', 'pvs', '--unbuffered', '--noheading', '-o', 'pv_name']
    process = subprocess.run(
        command,
        stdout=subprocess.PIPE)
    output = str(process.stdout, 'utf-8')

    volumes = []
    for volume in re.findall(r'(/dev/.*)\s$', output, re.M):
        shortname = re.match(r'/dev/(.*)', volume).group(1)
        volumes.append(
            {
                '{#SHORTNAME}': shortname,
                '{#VOLUME}': volume,
            }
        )

    return volumes


def volume_groups():
    """Returns the discovered volume groups.
    """
    command = ['sudo', 'vgs', '--unbuffered', '--noheading', '-o', 'vg_name']
    process = subprocess.run(
        command,
        stdout=subprocess.PIPE)
    output = str(process.stdout, 'utf-8')

    volumes = []
    for volume in re.findall(r'[a-z0-9-]+', output, re.M):
        volumes.append(
            {
                '{#SHORTNAME}': volume,
            }
        )

    return volumes


def logical_volumes():
    """Returns the discovered logical volumes.
    """
    command = ['sudo', 'lvs', '--unbuffered', '--noheading', '-o', 'lv_name,lv_path']
    process = subprocess.run(
        command,
        stdout=subprocess.PIPE)
    output = str(process.stdout, 'utf-8')

    volumes = []
    for volume in re.findall(r'[a-z0-9-]+ +/dev/[a-z0-9-/]+', output, re.M):
        name = re.match('([a-z0-9-]+)', volume).group(1)
        path = re.match('.*(/dev/.*)', volume).group(1)
        volumes.append(
            {
                '{#SHORTNAME}': name,
                '{#VOLUME}': path,
            }
        )

    return volumes

def main(switch=None):
    """Reads /etc/zabbix/urls.txt for URLs to monitor.
    """
    if switch == 'pv':
        volumes = physical_volumes()

    elif switch == 'vg':
        volumes = volume_groups()

    elif switch == 'lv':
        volumes = logical_volumes()

    else:
        volumes = []
    data = {'data': volumes}
    return json.dumps(data, sort_keys=True, indent=4)


if __name__ == '__main__':
    print(main(*sys.argv[1:]))
