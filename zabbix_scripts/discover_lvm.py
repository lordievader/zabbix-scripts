#!/usr/bin/env python3
""" Description: Discovers lvm related things.
Author:          Olivier van der Toorn <oliviervdtoorn@gmail.com>"""
import json
import re
import subprocess
import sys
import pdb


def check_lvm():
    """Checks if the necessary tools are available.
    """
    command = ['sudo', 'lvm', 'version']
    try:
        subprocess.check_call(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        passed = True

    except subprocess.CalledProcessError:
        passed = False

    return passed


def physical_volumes():
    """Returns the discovered physical volumes.
    """

    volumes = []
    if check_lvm() is True:
        command = [
            'sudo', 'pvs', '--unbuffered', '--noheading',
            '--nosuffix', '--reportformat', 'json',
            '-o', 'pv_name'
        ]
        process = subprocess.run(
            command,
            stdout=subprocess.PIPE)
        output = str(process.stdout, 'utf-8')
        if output:
            parsed = json.loads(output)['report'][0]['pv']
            for physical_volume in parsed:
                volume = physical_volume['pv_name']
                shortname = volume.split('/')[-1]
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
    volumes = []
    if check_lvm() is True:
        command = [
            'sudo', 'vgs', '--unbuffered', '--noheading',
            '--nosuffix', '--reportformat', 'json',
            '-o', 'vg_name'
        ]
        process = subprocess.run(
            command,
            stdout=subprocess.PIPE)
        output = str(process.stdout, 'utf-8')
        if output:
            parsed = json.loads(output)['report'][0]['vg']
            for volume_group in parsed:
                volumes.append(
                    {
                        '{#SHORTNAME}': volume_group['vg_name']
                    }
                )

    return volumes


def logical_volumes():
    """Uses `lvs` to discover the logical volumes and their paths.
    """
    volumes = []
    if check_lvm() is True:
        command = [
            'sudo', 'lvs', '--unbuffered', '--noheading',
            '--nosuffix', '--reportformat', 'json',
            '-o', 'lv_name,lv_path'
        ]
        process = subprocess.run(
            command,
            stdout=subprocess.PIPE)
        output = str(process.stdout, 'utf-8')
        if output:
            parsed = json.loads(output)['report'][0]['lv']
            for logical_volume in parsed:
                name = logical_volume['lv_name']
                if logical_volume['lv_path'] is '':
                    path = name

                else:
                    path = logical_volume['lv_path']

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
    print(main(*sys.argv[1:]))  # pragma: no cover
