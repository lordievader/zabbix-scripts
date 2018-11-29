#!/usr/bin/env python3
"""Description: Allows Zabbix to monitor lvm values
Author:         Olivier van der Toorn <oliviervdtoorn@gmail.com>
"""
import sys
import subprocess
import re

def sanitize(string):
    return re.sub(r'[^a-z0-9-_/]', '', string)

def filter_digits(string):
    return re.sub(r'[^0-9]', '', string)

def run_command(lvm, volume, option):
    volume = sanitize(volume)
    option = sanitize(option)
    command = [
        'sudo', lvm, '--unbuffered', '--noheadings', '--nosuffix',
        '--units', 'b', '-C', '-o', option, volume]
    process = subprocess.run(
        command,
        stdout=subprocess.PIPE)
    output = filter_digits(str(process.stdout, 'utf-8'))
    return output

def physical_volume(volume, option):
    return run_command('pvdisplay', volume, option)

def volume_group(volume, option):
    return run_command('vgdisplay', volume, option)

def logical_volume(volume, option):
    return run_command('lvdisplay', volume, option)

def main(*switch):
    output = ''
    if len(switch) == 3:
        if switch[0] == 'pv':
            output = physical_volume(switch[1], switch[2])

        elif switch[0] == 'vg':
            output = volume_group(switch[1], switch[2])

        elif switch[0] == 'lv':
            output = logical_volume(switch[1], switch[2])

    return output


if __name__ == '__main__':
    print(main(*sys.argv[1:]))
